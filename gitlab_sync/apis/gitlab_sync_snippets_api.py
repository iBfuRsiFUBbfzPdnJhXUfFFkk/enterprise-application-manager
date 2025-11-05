from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from gitlab import Gitlab

from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import (
    convert_and_enforce_utc_timezone,
)
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from gitlab_sync.models import (
    GitLabSyncJobTracker,
    GitLabSyncProject,
    GitLabSyncSnippet,
    GitLabSyncUser,
)
from gitlab_sync.utilities import (
    SyncResult,
    check_job_cancelled,
    handle_gitlab_api_errors,
    run_sync_in_background,
)


def _sync_snippets_background(
    request: HttpRequest, job_tracker: GitLabSyncJobTracker
) -> None:
    """Background function to sync snippets with progress tracking."""
    sync_result = SyncResult(
        entity_type="GitLabSyncSnippet", job_tracker_id=job_tracker.id
    )
    sync_result.add_log("Starting snippets sync...")

    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        sync_result.add_log("❌ Failed to get GitLab client")
        sync_result.add_failure("Failed to get GitLab client")
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return

    projects: QuerySet[GitLabSyncProject] = cast_query_set(
        typ=GitLabSyncProject,
        val=GitLabSyncProject.objects.all(),
    )

    project_count = projects.count()
    sync_result.add_log(f"Syncing snippets from {project_count} projects...")

    for proj_idx, project in enumerate(projects, 1):
        if check_job_cancelled(sync_result.job_tracker_id):
            sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
            sync_result.finish()
            print(f"[GitLabSync] {sync_result}")
            return

        sync_result.update_progress(
            proj_idx - 1,
            project_count,
            f"📥 Fetching snippets from project {project.path_with_namespace} ({proj_idx}/{project_count})...",
        )

        snippets, error = handle_gitlab_api_errors(
            func=lambda: [
                s.asdict()
                for s in git_lab_client.projects.get(id=project.id, lazy=True)
                .snippets.list(get_all=True)
            ],
            entity_name=f"Snippets for project {project.path_with_namespace}",
            max_retries=3,
        )

        if error:
            error_str = str(error).lower()
            if "403" in error_str or "forbidden" in error_str:
                sync_result.add_log(
                    f"⚠️ Access denied for snippets in {project.path_with_namespace} - skipping"
                )
                continue
            sync_result.add_log(
                f"❌ Error fetching snippets for {project.path_with_namespace}: {error}"
            )
            sync_result.add_failure(error)
            continue

        if not snippets:
            continue

        sync_result.add_log(
            f"✓ Fetched {len(snippets)} snippets from {project.path_with_namespace}"
        )

        for snippet_dict in snippets:
            if check_job_cancelled(sync_result.job_tracker_id):
                sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
                sync_result.finish()
                print(f"[GitLabSync] {sync_result}")
                return

            gitlab_id: int | None = snippet_dict.get("id")
            if gitlab_id is None:
                sync_result.add_skip()
                continue

            try:
                snippet, created = GitLabSyncSnippet.objects.get_or_create(
                    gitlab_id=gitlab_id, defaults={"project": project}
                )

                snippet.project = project
                snippet.title = snippet_dict.get("title")
                snippet.file_name = snippet_dict.get("file_name")
                snippet.description = snippet_dict.get("description")
                snippet.visibility = snippet_dict.get("visibility")
                snippet.web_url = snippet_dict.get("web_url")
                snippet.raw_url = snippet_dict.get("raw_url")
                snippet.created_at = convert_and_enforce_utc_timezone(
                    datetime_string=snippet_dict.get("created_at")
                )
                snippet.updated_at = convert_and_enforce_utc_timezone(
                    datetime_string=snippet_dict.get("updated_at")
                )

                # Handle author
                author_dict = snippet_dict.get("author")
                if author_dict:
                    author_id = author_dict.get("id")
                    if author_id:
                        snippet.author = GitLabSyncUser.objects.filter(
                            id=author_id
                        ).first()

                snippet.save()
                sync_result.add_success()

            except Exception as error:
                import traceback

                error_trace = traceback.format_exc()
                error_msg = f"Failed to save snippet {gitlab_id}: {str(error)}"
                sync_result.add_failure(error_msg)
                sync_result.add_log(f"❌ {error_msg}")
                print(f"[GitLabSync] {error_msg}\n{error_trace}")
                continue

    sync_result.update_progress(project_count, project_count, None)
    sync_result.add_log(
        f"✓ Sync complete: {sync_result.synced_count} synced, {sync_result.skipped_count} skipped, {sync_result.failed_count} failed"
    )
    sync_result.finish()
    print(f"[GitLabSync] {sync_result}")


def gitlab_sync_snippets_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Sync snippets from GitLab EE 17.11.6 with background job tracking.

    Snippets are code or text fragments stored in GitLab.

    Returns immediately with job_id for progress tracking.
    """
    job_tracker = run_sync_in_background("snippets", _sync_snippets_background, request)

    return JsonResponse(
        data={"success": True, "job_id": job_tracker.id, "job_type": "snippets"}
    )
