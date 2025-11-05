from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from gitlab import Gitlab

from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import (
    convert_and_enforce_utc_timezone,
)
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from gitlab_sync.models import (
    GitLabSyncEvent,
    GitLabSyncJobTracker,
    GitLabSyncProject,
    GitLabSyncUser,
)
from gitlab_sync.utilities import (
    SyncResult,
    check_job_cancelled,
    handle_gitlab_api_errors,
    run_sync_in_background,
)


def _sync_events_background(
    request: HttpRequest, job_tracker: GitLabSyncJobTracker
) -> None:
    """Background function to sync events with progress tracking."""
    sync_result = SyncResult(
        entity_type="GitLabSyncEvent", job_tracker_id=job_tracker.id
    )
    sync_result.add_log("Starting events sync...")

    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        sync_result.add_log("❌ Failed to get GitLab client")
        sync_result.add_failure("Failed to get GitLab client")
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return

    config = ThisServerConfiguration.current()
    max_events = config.coerced_gitlab_sync_max_events_per_project

    projects: QuerySet[GitLabSyncProject] = cast_query_set(
        typ=GitLabSyncProject,
        val=GitLabSyncProject.objects.all(),
    )

    project_count = projects.count()
    sync_result.add_log(
        f"Syncing events from {project_count} projects (max {max_events} per project)..."
    )

    for proj_idx, project in enumerate(projects, 1):
        # Check if job was cancelled
        if check_job_cancelled(sync_result.job_tracker_id):
            sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
            sync_result.finish()
            print(f"[GitLabSync] {sync_result}")
            return

        # Update progress at project level
        sync_result.update_progress(
            proj_idx - 1,
            project_count,
            f"📥 About to fetch events from project {project.path_with_namespace} (project {proj_idx}/{project_count})...",
        )

        # Calculate pagination: if max_events < 100, use max_events as per_page
        # Otherwise use 100 per page and calculate max_pages
        if max_events <= 100:
            per_page = max_events
            max_pages = 1
        else:
            per_page = 100
            max_pages = (max_events + 99) // 100  # Ceiling division

        events, error = handle_gitlab_api_errors(
            func=lambda: [
                e.asdict()
                for e in git_lab_client.projects.get(id=project.id, lazy=True)
                .events.list(per_page=per_page, max_pages=max_pages)
            ][:max_events],  # Slice to exact limit
            entity_name=f"Events for project {project.path_with_namespace}",
            max_retries=3,
        )

        if error:
            # Check if this is a 403 Forbidden error - if so, just log and continue without failing
            error_str = str(error).lower()
            if (
                "403" in error_str
                or "forbidden" in error_str
                or "access denied" in error_str
                or "permission denied" in error_str
            ):
                sync_result.add_log(
                    f"⚠️ Access denied (403) for events in {project.path_with_namespace} - skipping"
                )
                continue

            # For other errors, add as failure
            sync_result.add_log(
                f"❌ Error fetching events for {project.path_with_namespace}: {error}"
            )
            sync_result.add_failure(error)
            continue

        if not events:
            sync_result.add_log(f"⊘ No events found in project {project.path_with_namespace}")
            continue

        sync_result.add_log(f"✓ Fetched {len(events)} events from {project.path_with_namespace}, about to process...")

        # Process each event immediately
        for event_dict in events:
            # Check if job was cancelled
            if check_job_cancelled(sync_result.job_tracker_id):
                sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
                sync_result.finish()
                print(f"[GitLabSync] {sync_result}")
                return

            event_id: int | None = event_dict.get("id")

            if event_id is None:
                sync_result.add_skip()
                continue

            try:
                sync_result.add_log(f"💾 About to get_or_create event {event_id} in database...")
                event, created = GitLabSyncEvent.objects.get_or_create(
                    gitlab_id=event_id
                )
                sync_result.add_log(f"✓ Database get_or_create succeeded for event {event_id} (created={created})")

                # Events don't have updated_at, so we update if created
                if not created:
                    sync_result.add_skip()
                    sync_result.add_log(f"⊘ Skipped existing event #{event_id}")
                    continue

                # Update event fields
                event.project = GitLabSyncProject.objects.filter(
                    id=project.id
                ).first()

                # Handle author
                author_dict = event_dict.get("author")
                if author_dict:
                    user = GitLabSyncUser.objects.filter(id=author_dict.get("id")).first()
                    if user:
                        event.author = user

                event.action_name = event_dict.get("action_name")
                event.target_id = event_dict.get("target_id")
                event.target_iid = event_dict.get("target_iid")
                event.target_type = event_dict.get("target_type")
                event.target_title = event_dict.get("target_title")
                event.title = event_dict.get("title")

                # Handle push data
                push_data = event_dict.get("push_data", {})
                if push_data:
                    event.push_data_commit_count = push_data.get("commit_count")
                    event.push_data_action = push_data.get("action")
                    event.push_data_ref_type = push_data.get("ref_type")
                    event.push_data_commit_from = push_data.get("commit_from")
                    event.push_data_commit_to = push_data.get("commit_to")
                    event.push_data_ref = push_data.get("ref")
                    event.push_data_commit_title = push_data.get("commit_title")

                event.created_at = convert_and_enforce_utc_timezone(
                    datetime_string=event_dict.get("created_at")
                )

                sync_result.add_log(f"💾 About to save event {event_id} to database...")
                event.save()
                sync_result.add_log(f"✓ Database save succeeded for event {event_id}")

                sync_result.add_success()

            except Exception as error:
                import traceback
                error_trace = traceback.format_exc()
                error_msg = f"Failed to save event {event_id}: {str(error)}"
                sync_result.add_failure(error_msg)
                sync_result.add_log(f"❌ {error_msg}")
                print(f"[GitLabSync] {error_msg}")
                print(f"[GitLabSync] Stack trace:\n{error_trace}")
                continue

    # Final progress update
    sync_result.update_progress(project_count, project_count, None)

    sync_result.add_log(
        f"✓ Sync complete: {sync_result.synced_count} synced, "
        f"{sync_result.skipped_count} skipped, {sync_result.failed_count} failed"
    )
    sync_result.finish()
    print(f"[GitLabSync] {sync_result}")


def gitlab_sync_events_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Sync events from GitLab EE 17.11.6 with background job tracking.

    Tracks project activity events like pushes, issues, merge requests, etc.

    Returns immediately with job_id for progress tracking.
    """
    job_tracker = run_sync_in_background("events", _sync_events_background, request)

    return JsonResponse(
        data={"success": True, "job_id": job_tracker.id, "job_type": "events"}
    )
