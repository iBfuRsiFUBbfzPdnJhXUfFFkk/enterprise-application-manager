from typing import cast

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab
from gitlab.v4.objects import Group, GroupProject

from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import convert_and_enforce_utc_timezone
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.models.common.typed_dicts.git_lab_links_typed_dict import GitLabLinksTypedDict
from git_lab.models.common.typed_dicts.git_lab_namespace_typed_dict import GitLabNamespaceTypedDict
from git_lab.models.common.typed_dicts.git_lab_project_typed_dict import GitLabProjectTypedDict
from git_lab.models.git_lab_group import GitLabGroup
from git_lab.models.git_lab_project import GitLabProject


def git_lab_projects_api(
        request: HttpRequest,
) -> JsonResponse | HttpResponse:
    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        return generic_500(request=request)
    git_lab_groups: QuerySet[GitLabGroup] = cast_query_set(
        typ=GitLabGroup,
        val=GitLabGroup.objects.all(),
    )
    all_projects: set[GroupProject] = set()
    for git_lab_group in git_lab_groups:
        group: Group | None = git_lab_client.groups.get(id=git_lab_group.id)
        if group is None:
            continue
        projects: list[GroupProject] = cast(typ=list[GroupProject], val=group.projects.list(all=True))
        for project in projects:
            all_projects.add(project)
    project_dicts: list[GitLabProjectTypedDict] = [project.asdict() for project in list(all_projects)]
    for project_dict in project_dicts:
        project_id: int | None = project_dict.get("id")
        if project_id is None:
            continue
        git_lab_project: GitLabProject = GitLabProject.objects.get_or_create(id=project_id)[0]
        git_lab_project.avatar_url = project_dict.get("avatar_url")
        git_lab_project.container_registry_image_prefix = project_dict.get("container_registry_image_prefix")
        git_lab_project.created_at = convert_and_enforce_utc_timezone(datetime_string=project_dict.get("created_at"))
        git_lab_project.default_branch = project_dict.get("default_branch")
        git_lab_project.description = project_dict.get("description")
        git_lab_project.http_url_to_repo = project_dict.get("http_url_to_repo")
        git_lab_project.last_activity_at = convert_and_enforce_utc_timezone(
            datetime_string=project_dict.get("last_activity_at"))
        links: GitLabLinksTypedDict | None = project_dict.get("_links")
        if links is not None:
            git_lab_project.link_cluster_agents = links.get("cluster_agents")
            git_lab_project.link_events = links.get("events")
            git_lab_project.link_issues = links.get("issues")
            git_lab_project.link_labels = links.get("labels")
            git_lab_project.link_members = links.get("members")
            git_lab_project.link_merge_requests = links.get("merge_requests")
            git_lab_project.link_repo_branches = links.get("repo_branches")
            git_lab_project.link_self = links.get("self")
        git_lab_project.name = project_dict.get("name")
        git_lab_project.name_with_namespace = project_dict.get("name_with_namespace")
        namespace: GitLabNamespaceTypedDict | None = project_dict.get("namespace")
        if namespace is not None:
            namespace_id: int | None = namespace.get("id")
            namespace_kind: str | None = namespace.get("kind")
            if namespace_kind == "group":
                group: GitLabGroup | None = GitLabGroup.objects.filter(id=namespace_id).first()
                if group is not None:
                    git_lab_project.group = group
        git_lab_project.open_issues_count = project_dict.get("open_issues_count")
        git_lab_project.path = project_dict.get("path")
        git_lab_project.path_with_namespace = project_dict.get("path_with_namespace")
        git_lab_project.readme_url = project_dict.get("readme_url")
        git_lab_project.ssh_url_to_repo = project_dict.get("ssh_url_to_repo")
        git_lab_project.updated_at = convert_and_enforce_utc_timezone(datetime_string=project_dict.get("updated_at"))
        git_lab_project.web_url = project_dict.get("web_url")
        git_lab_project.save()
    return JsonResponse(data=project_dicts, safe=False)
