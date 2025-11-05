from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from gitlab import Gitlab

from core.utilities.cast_query_set import cast_query_set
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from gitlab_sync.models import (
    GitLabSyncJobTracker,
    GitLabSyncProject,
    GitLabSyncRepository,
)
from gitlab_sync.utilities import (
    SyncResult,
    check_job_cancelled,
    handle_gitlab_api_errors,
    run_sync_in_background,
)


def _sync_repositories_background(
    request: HttpRequest, job_tracker: GitLabSyncJobTracker
) -> None:
    """Background function to sync repositories with progress tracking."""
    sync_result = SyncResult(
        entity_type="GitLabSyncRepository", job_tracker_id=job_tracker.id
    )
    sync_result.add_log("Starting repositories sync...")

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
    sync_result.add_log(
        f"Syncing repositories from {project_count} projects..."
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
            f"📥 About to fetch repository from project {project.path_with_namespace} (project {proj_idx}/{project_count})...",
        )

        # Fetch project with statistics
        project_data, error = handle_gitlab_api_errors(
            func=lambda: git_lab_client.projects.get(id=project.id, statistics=True).asdict(),
            entity_name=f"Repository for project {project.path_with_namespace}",
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
                    f"⚠️ Access denied (403) for repository in {project.path_with_namespace} - skipping"
                )
                continue

            # For other errors, add as failure
            sync_result.add_log(
                f"❌ Error fetching repository for {project.path_with_namespace}: {error}"
            )
            sync_result.add_failure(error)
            continue

        if not project_data:
            sync_result.add_log(f"⊘ No repository data found for project {project.path_with_namespace}")
            continue

        try:
            sync_result.add_log(f"💾 About to get_or_create repository for {project.path_with_namespace}...")
            repository, created = GitLabSyncRepository.objects.get_or_create(
                project=project,
                defaults={"name": f"{project.name} Repository"}
            )
            sync_result.add_log(f"✓ Database get_or_create succeeded for repository (created={created})")

            # Update repository fields
            repository.name = f"{project.name} Repository"
            repository.default_branch = project_data.get("default_branch")
            repository.http_url_to_repo = project_data.get("http_url_to_repo")
            repository.ssh_url_to_repo = project_data.get("ssh_url_to_repo")

            # Handle statistics
            statistics = project_data.get("statistics", {})
            if statistics:
                repository.repository_size = statistics.get("repository_size")
                repository.lfs_size = statistics.get("lfs_objects_size")
                repository.storage_size = statistics.get("storage_size")
                repository.wiki_size = statistics.get("wiki_size")
                repository.packages_size = statistics.get("packages_size")
                repository.snippets_size = statistics.get("snippets_size")

            sync_result.add_log(f"💾 About to save repository for {project.path_with_namespace}...")
            repository.save()
            sync_result.add_log(f"✓ Database save succeeded for repository")
            sync_result.add_success()

        except Exception as error:
            import traceback
            error_trace = traceback.format_exc()
            error_msg = f"Failed to save repository for {project.path_with_namespace}: {str(error)}"
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


def gitlab_sync_repositories_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Sync repositories from GitLab EE 17.11.6 with background job tracking.

    New functionality not present in the original git_lab app.
    Tracks repository metadata and storage statistics.

    Returns immediately with job_id for progress tracking.
    """
    job_tracker = run_sync_in_background("repositories", _sync_repositories_background, request)

    return JsonResponse(
        data={"success": True, "job_id": job_tracker.id, "job_type": "repositories"}
    )
