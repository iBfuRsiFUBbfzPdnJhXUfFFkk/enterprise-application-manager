from datetime import timedelta

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone
from gitlab import Gitlab

from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import (
    convert_and_enforce_utc_timezone,
)
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from gitlab_sync.models import (
    GitLabSyncCommit,
    GitLabSyncJobTracker,
    GitLabSyncProject,
    GitLabSyncRepository,
    GitLabSyncUser,
)
from gitlab_sync.utilities import (
    SyncResult,
    check_job_cancelled,
    handle_gitlab_api_errors,
    run_sync_in_background,
)


def _sync_commits_background(
    request: HttpRequest, job_tracker: GitLabSyncJobTracker
) -> None:
    """Background function to sync commits with progress tracking."""
    sync_result = SyncResult(
        entity_type="GitLabSyncCommit", job_tracker_id=job_tracker.id
    )
    sync_result.add_log("Starting commits sync...")

    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        sync_result.add_log("❌ Failed to get GitLab client")
        sync_result.add_failure("Failed to get GitLab client")
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return

    config = ThisServerConfiguration.current()
    days_back = config.coerced_gitlab_sync_commits_days_back

    # Calculate date cutoff for filtering commits
    cutoff_date = timezone.now() - timedelta(days=days_back)

    projects: QuerySet[GitLabSyncProject] = cast_query_set(
        typ=GitLabSyncProject,
        val=GitLabSyncProject.objects.all(),
    )

    project_count = projects.count()
    sync_result.add_log(
        f"Syncing commits from {project_count} projects incrementally (last {days_back} days)..."
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
            f"📥 About to fetch commits from project {project.path_with_namespace} (project {proj_idx}/{project_count})...",
        )

        commits, error = handle_gitlab_api_errors(
            func=lambda: [
                c.asdict()
                for c in git_lab_client.projects.get(id=project.id, lazy=True)
                .commits.list(since=cutoff_date.isoformat(), get_all=True)
            ],
            entity_name=f"Commits for project {project.path_with_namespace}",
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
                    f"⚠️ Access denied (403) for commits in {project.path_with_namespace} - skipping"
                )
                continue

            # For other errors, add as failure
            sync_result.add_log(
                f"❌ Error fetching commits for {project.path_with_namespace}: {error}"
            )
            sync_result.add_failure(error)
            continue

        if not commits:
            sync_result.add_log(f"⊘ No commits found in project {project.path_with_namespace}")
            continue

        sync_result.add_log(f"✓ Fetched {len(commits)} commits from {project.path_with_namespace}, about to process...")

        # Get or create repository for this project
        repository = None
        try:
            repository, _ = GitLabSyncRepository.objects.get_or_create(
                project=project,
                defaults={"name": f"{project.name} Repository"}
            )
        except Exception as repo_error:
            sync_result.add_log(f"⚠️ Could not create repository for project {project.id}: {repo_error}")

        # Process each commit immediately
        for commit_dict in commits:
            # Check if job was cancelled
            if check_job_cancelled(sync_result.job_tracker_id):
                sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
                sync_result.finish()
                print(f"[GitLabSync] {sync_result}")
                return

            commit_sha: str | None = commit_dict.get("id")

            if commit_sha is None:
                sync_result.add_skip()
                continue

            try:
                sync_result.add_log(f"💾 About to get_or_create commit {commit_sha[:8]} in database...")
                commit, created = GitLabSyncCommit.objects.get_or_create(
                    sha=commit_sha,
                    defaults={"project": project}
                )
                sync_result.add_log(f"✓ Database get_or_create succeeded for commit {commit_sha[:8]} (created={created})")

                # Check if we need to update (commits rarely change, but we'll check created_at)
                commit_created_at = convert_and_enforce_utc_timezone(
                    datetime_string=commit_dict.get("created_at")
                )

                needs_update = created or (
                    commit.last_synced_at is None
                    or (
                        commit_created_at
                        and commit_created_at > commit.last_synced_at
                    )
                )

                if not needs_update:
                    sync_result.add_skip()
                    sync_result.add_log(f"⊘ Skipped unchanged commit {commit_sha[:8]}")
                    continue

                # Update commit fields
                commit.project = project
                if repository:
                    commit.repository = repository

                commit.sha = commit_sha
                commit.short_id = commit_dict.get("short_id")
                commit.title = commit_dict.get("title")
                commit.message = commit_dict.get("message")
                commit.author_name = commit_dict.get("author_name")
                commit.author_email = commit_dict.get("author_email")
                commit.committer_name = commit_dict.get("committer_name")
                commit.committer_email = commit_dict.get("committer_email")
                commit.web_url = commit_dict.get("web_url")

                # Handle parent IDs
                parent_ids = commit_dict.get("parent_ids", [])
                if parent_ids:
                    commit.parent_ids = ",".join(parent_ids)

                # Handle stats
                stats = commit_dict.get("stats", {})
                if stats:
                    commit.additions = stats.get("additions")
                    commit.deletions = stats.get("deletions")
                    commit.total_changes = stats.get("total")

                commit.created_at = commit_created_at
                commit.authored_date = convert_and_enforce_utc_timezone(
                    datetime_string=commit_dict.get("authored_date")
                )
                commit.committed_date = convert_and_enforce_utc_timezone(
                    datetime_string=commit_dict.get("committed_date")
                )
                commit.last_synced_at = timezone.now()

                sync_result.add_log(f"💾 About to save commit {commit_sha[:8]} to database...")
                commit.save()
                sync_result.add_log(f"✓ Database save succeeded for commit {commit_sha[:8]}")
                sync_result.add_success()

            except Exception as error:
                import traceback
                error_trace = traceback.format_exc()
                error_msg = f"Failed to save commit {commit_sha[:8] if commit_sha else 'unknown'}: {str(error)}"
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


def gitlab_sync_commits_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Sync commits from GitLab EE 17.11.6 with background job tracking.

    New functionality not present in the original git_lab app.
    Tracks individual commits and code changes.

    Returns immediately with job_id for progress tracking.
    """
    job_tracker = run_sync_in_background("commits", _sync_commits_background, request)

    return JsonResponse(
        data={"success": True, "job_id": job_tracker.id, "job_type": "commits"}
    )
