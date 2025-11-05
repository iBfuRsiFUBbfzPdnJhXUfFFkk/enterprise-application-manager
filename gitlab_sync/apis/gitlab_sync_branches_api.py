from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from gitlab import Gitlab

from core.utilities.cast_query_set import cast_query_set
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from gitlab_sync.models import (
    GitLabSyncBranch,
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


def _sync_branches_background(
    request: HttpRequest, job_tracker: GitLabSyncJobTracker
) -> None:
    """Background function to sync branches with progress tracking."""
    sync_result = SyncResult(
        entity_type="GitLabSyncBranch", job_tracker_id=job_tracker.id
    )
    sync_result.add_log("Starting branches sync...")

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
        f"Syncing branches from {project_count} projects..."
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
            f"📥 About to fetch branches from project {project.path_with_namespace} (project {proj_idx}/{project_count})...",
        )

        branches, error = handle_gitlab_api_errors(
            func=lambda: [
                b.asdict()
                for b in git_lab_client.projects.get(id=project.id, lazy=True)
                .branches.list(get_all=True)
            ],
            entity_name=f"Branches for project {project.path_with_namespace}",
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
                    f"⚠️ Access denied (403) for branches in {project.path_with_namespace} - skipping"
                )
                continue

            # For other errors, add as failure
            sync_result.add_log(
                f"❌ Error fetching branches for {project.path_with_namespace}: {error}"
            )
            sync_result.add_failure(error)
            continue

        if not branches:
            sync_result.add_log(f"⊘ No branches found in project {project.path_with_namespace}")
            continue

        sync_result.add_log(f"✓ Fetched {len(branches)} branches from {project.path_with_namespace}, about to process...")

        # Get or create repository for this project
        repository = None
        try:
            repository, _ = GitLabSyncRepository.objects.get_or_create(
                project=project,
                defaults={"name": f"{project.name} Repository"}
            )
        except Exception as repo_error:
            sync_result.add_log(f"⚠️ Could not create repository for project {project.id}: {repo_error}")

        # Process each branch immediately
        for branch_dict in branches:
            # Check if job was cancelled
            if check_job_cancelled(sync_result.job_tracker_id):
                sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
                sync_result.finish()
                print(f"[GitLabSync] {sync_result}")
                return

            branch_name: str | None = branch_dict.get("name")

            if branch_name is None:
                sync_result.add_skip()
                continue

            try:
                sync_result.add_log(f"💾 About to get_or_create branch {branch_name} in database...")
                branch, created = GitLabSyncBranch.objects.get_or_create(
                    project=project,
                    name=branch_name,
                    defaults={}
                )
                sync_result.add_log(f"✓ Database get_or_create succeeded for branch {branch_name} (created={created})")

                # Update branch fields
                branch.project = project
                if repository:
                    branch.repository = repository

                branch.name = branch_name
                branch.merged = branch_dict.get("merged")
                branch.protected = branch_dict.get("protected")
                branch.default = branch_dict.get("default")
                branch.developers_can_push = branch_dict.get("developers_can_push")
                branch.developers_can_merge = branch_dict.get("developers_can_merge")
                branch.can_push = branch_dict.get("can_push")
                branch.web_url = branch_dict.get("web_url")

                # Handle commit info
                commit = branch_dict.get("commit", {})
                if commit:
                    branch.commit_sha = commit.get("id")
                    branch.commit_short_id = commit.get("short_id")
                    branch.commit_title = commit.get("title")
                    branch.commit_message = commit.get("message")

                sync_result.add_log(f"💾 About to save branch {branch_name} to database...")
                branch.save()
                sync_result.add_log(f"✓ Database save succeeded for branch {branch_name}")
                sync_result.add_success()

            except Exception as error:
                import traceback
                error_trace = traceback.format_exc()
                error_msg = f"Failed to save branch {branch_name if branch_name else 'unknown'}: {str(error)}"
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


def gitlab_sync_branches_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Sync branches from GitLab EE 17.11.6 with background job tracking.

    New functionality not present in the original git_lab app.
    Tracks Git branches and their status.

    Returns immediately with job_id for progress tracking.
    """
    job_tracker = run_sync_in_background("branches", _sync_branches_background, request)

    return JsonResponse(
        data={"success": True, "job_id": job_tracker.id, "job_type": "branches"}
    )
