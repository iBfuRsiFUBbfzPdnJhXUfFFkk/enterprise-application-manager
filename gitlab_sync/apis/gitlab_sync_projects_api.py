from typing import cast

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from gitlab import Gitlab
from gitlab.v4.objects import Group, GroupProject

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
from gitlab_sync.models import GitLabSyncGroup, GitLabSyncProject
from gitlab_sync.utilities import SyncResult, handle_gitlab_api_errors


def gitlab_sync_projects_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Sync GitLab projects from GitLab EE 17.11.6 with improved error handling.

    This API endpoint fetches projects from all GitLab groups and syncs them
    to the local database with enhanced error handling and retry logic.
    """
    sync_result = SyncResult(entity_type="GitLabSyncProject")

    query_parameters: GitLabApiCommonQueryParameters = get_common_query_parameters(
        request=request
    )

    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        sync_result.add_failure("Failed to get GitLab client")
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return generic_500(request=request)

    git_lab_groups: QuerySet[GitLabSyncGroup] = cast_query_set(
        typ=GitLabSyncGroup,
        val=GitLabSyncGroup.objects.all(),
    )

    if not git_lab_groups.exists():
        sync_result.add_failure(
            "No groups found - please sync groups first using the 'Sync Groups' button"
        )
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return JsonResponse(data=sync_result.to_dict(), safe=False, status=400)

    all_projects: set[GroupProject] = set()

    for git_lab_group in git_lab_groups:
        projects, error = handle_gitlab_api_errors(
            func=lambda: cast(
                list[GroupProject],
                git_lab_client.groups.get(id=git_lab_group.id).projects.list(
                    **query_parameters
                ),
            ),
            entity_name=f"Projects for group {git_lab_group.full_path}",
            max_retries=3,
        )

        if error:
            sync_result.add_failure(error)
            continue

        if projects:
            all_projects.update(projects)

    project_dicts: list[dict] = [project.asdict() for project in list(all_projects)]

    for project_dict in project_dicts:
        project_id: int | None = project_dict.get("id")
        if project_id is None:
            sync_result.add_skip()
            continue

        try:
            git_lab_project, created = GitLabSyncProject.objects.get_or_create(
                id=project_id
            )

            git_lab_project.avatar_url = project_dict.get("avatar_url")
            git_lab_project.container_registry_image_prefix = project_dict.get(
                "container_registry_image_prefix"
            )
            git_lab_project.default_branch = project_dict.get("default_branch") or "main"
            git_lab_project.description = project_dict.get("description")
            git_lab_project.http_url_to_repo = project_dict.get("http_url_to_repo")
            git_lab_project.name = project_dict.get("name")
            git_lab_project.name_with_namespace = project_dict.get(
                "name_with_namespace"
            )
            git_lab_project.open_issues_count = project_dict.get("open_issues_count") or 0
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
            git_lab_project.updated_at = convert_and_enforce_utc_timezone(
                datetime_string=project_dict.get("updated_at")
            )

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

        except Exception as error:
            error_msg = f"Failed to save project {project_id}: {str(error)}"
            sync_result.add_failure(error_msg)
            continue

    sync_result.finish()
    print(f"[GitLabSync] {sync_result}")

    return JsonResponse(data=sync_result.to_dict(), safe=False)
