from typing import cast

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from gitlab import Gitlab
from gitlab.v4.objects import Group, GroupProject

from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import (
    convert_and_enforce_utc_timezone,
)
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.apis.common.get_common_query_parameters import (
    GitLabApiCommonQueryParameters,
    get_common_query_parameters,
)
from gitlab_sync.models import GitLabSyncGroup, GitLabSyncJobTracker, GitLabSyncProject
from gitlab_sync.utilities import (
    SyncResult,
    check_job_cancelled,
    handle_gitlab_api_errors,
    run_sync_in_background,
)


def _sync_projects_background(
    request: HttpRequest, job_tracker: GitLabSyncJobTracker
) -> None:
    """Background function to sync projects with progress tracking."""
    sync_result = SyncResult(
        entity_type="GitLabSyncProject", job_tracker_id=job_tracker.id
    )
    sync_result.add_log("Starting projects sync...")

    query_parameters: GitLabApiCommonQueryParameters = get_common_query_parameters(
        request=request
    )

    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        sync_result.add_log("❌ Failed to get GitLab client")
        sync_result.add_failure("Failed to get GitLab client")
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return

    git_lab_groups: QuerySet[GitLabSyncGroup] = cast_query_set(
        typ=GitLabSyncGroup,
        val=GitLabSyncGroup.objects.all(),
    )

    if not git_lab_groups.exists():
        sync_result.add_log(
            "❌ No groups found - please sync groups first using the 'Sync Groups' button"
        )
        sync_result.add_failure(
            "No groups found - please sync groups first using the 'Sync Groups' button"
        )
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return

    from datetime import datetime

    config = ThisServerConfiguration.current()
    max_projects_per_group = config.coerced_gitlab_sync_max_projects_per_group

    group_count = git_lab_groups.count()
    sync_result.add_log(
        f"Syncing projects from {group_count} groups incrementally (max {max_projects_per_group} per group)..."
    )

    # Update query params to limit projects per group
    limited_query_parameters = {**query_parameters, "per_page": max_projects_per_group}

    processed_count = 0
    estimated_total = group_count * 10  # Rough estimate

    for group_idx, git_lab_group in enumerate(git_lab_groups, 1):
        # Check if job was cancelled
        if check_job_cancelled(sync_result.job_tracker_id):
            sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
            sync_result.finish()
            print(f"[GitLabSync] {sync_result}")
            return

        projects, error = handle_gitlab_api_errors(
            func=lambda: cast(
                list[GroupProject],
                git_lab_client.groups.get(id=git_lab_group.id).projects.list(
                    **limited_query_parameters
                ),
            ),
            entity_name=f"Projects for group {git_lab_group.full_path}",
            max_retries=3,
        )

        if error:
            sync_result.add_log(
                f"❌ Error fetching projects for {git_lab_group.full_path}: {error}"
            )
            sync_result.add_failure(error)
            continue

        if not projects:
            continue

        # Process each project immediately
        for project in projects:
            # Check if job was cancelled
            if check_job_cancelled(sync_result.job_tracker_id):
                sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
                sync_result.finish()
                print(f"[GitLabSync] {sync_result}")
                return

            processed_count += 1
            project_dict = project.asdict()
            project_id: int | None = project_dict.get("id")

            if project_id is None:
                sync_result.add_skip()
                continue

            try:
                git_lab_project, created = GitLabSyncProject.objects.get_or_create(
                    id=project_id
                )

                # Check if we need to update (compare updated_at from GitLab with our last_synced_at)
                project_updated_at = convert_and_enforce_utc_timezone(
                    datetime_string=project_dict.get("updated_at")
                )

                needs_update = created or (
                    git_lab_project.last_synced_at is None
                    or (
                        project_updated_at
                        and project_updated_at > git_lab_project.last_synced_at
                    )
                )

                if not needs_update:
                    sync_result.add_skip()
                    sync_result.update_progress(
                        processed_count,
                        estimated_total,
                        f"⊘ Skipped unchanged project {project_dict.get('path_with_namespace')}",
                    )
                    continue

                # Update project fields
                git_lab_project.avatar_url = project_dict.get("avatar_url")
                git_lab_project.container_registry_image_prefix = project_dict.get(
                    "container_registry_image_prefix"
                )
                git_lab_project.default_branch = (
                    project_dict.get("default_branch") or "main"
                )
                git_lab_project.description = project_dict.get("description")
                git_lab_project.http_url_to_repo = project_dict.get("http_url_to_repo")
                git_lab_project.name = project_dict.get("name")
                git_lab_project.name_with_namespace = project_dict.get(
                    "name_with_namespace"
                )
                git_lab_project.open_issues_count = (
                    project_dict.get("open_issues_count") or 0
                )
                git_lab_project.path = project_dict.get("path")
                git_lab_project.path_with_namespace = project_dict.get(
                    "path_with_namespace"
                )
                git_lab_project.readme_url = project_dict.get("readme_url")
                git_lab_project.ssh_url_to_repo = project_dict.get("ssh_url_to_repo")
                git_lab_project.web_url = project_dict.get("web_url")
                git_lab_project.visibility = project_dict.get("visibility")
                git_lab_project.archived = project_dict.get("archived")
                git_lab_project.star_count = project_dict.get("star_count") or 0
                git_lab_project.forks_count = project_dict.get("forks_count") or 0

                git_lab_project.created_at = convert_and_enforce_utc_timezone(
                    datetime_string=project_dict.get("created_at")
                )
                git_lab_project.last_activity_at = convert_and_enforce_utc_timezone(
                    datetime_string=project_dict.get("last_activity_at")
                )
                git_lab_project.updated_at = project_updated_at
                git_lab_project.last_synced_at = datetime.now()

                namespace = project_dict.get("namespace")
                if namespace:
                    namespace_id = namespace.get("id")
                    namespace_kind = namespace.get("kind")
                    if namespace_kind == "group":
                        group = GitLabSyncGroup.objects.filter(id=namespace_id).first()
                        if group:
                            git_lab_project.group = group

                git_lab_project.save()
                sync_result.add_success()
                sync_result.update_progress(
                    processed_count,
                    estimated_total,
                    f"✓ Synced project {git_lab_project.name_with_namespace}",
                )

            except Exception as error:
                error_msg = f"Failed to save project {project_id}: {str(error)}"
                sync_result.add_failure(error_msg)
                sync_result.add_log(f"❌ {error_msg}")
                continue

        # Update estimate based on actual projects found
        estimated_total = max(estimated_total, processed_count + (group_count - group_idx) * 10)

    sync_result.add_log(
        f"✓ Sync complete: {sync_result.synced_count} synced, "
        f"{sync_result.skipped_count} skipped, {sync_result.failed_count} failed"
    )
    sync_result.finish()
    print(f"[GitLabSync] {sync_result}")


def gitlab_sync_projects_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Sync GitLab projects from GitLab EE 17.11.6 with background job tracking.

    This API endpoint fetches projects from all GitLab groups and syncs them
    to the local database with enhanced error handling and retry logic.

    Returns immediately with job_id for progress tracking.
    """
    job_tracker = run_sync_in_background("projects", _sync_projects_background, request)

    return JsonResponse(
        data={"success": True, "job_id": job_tracker.id, "job_type": "projects"}
    )
