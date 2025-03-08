from typing import cast, TypedDict

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab
from gitlab.v4.objects import Group, GroupProject

from core.utilities.cast_query_set import cast_query_set
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.models.git_lab_group import GitLabGroup
from git_lab.models.git_lab_project import GitLabProject


class GitLabProjectLinksTypedDict(TypedDict):
    cluster_agents: str | None
    events: str | None
    issues: str | None
    labels: str | None
    members: str | None
    merge_requests: str | None
    repo_branches: str | None
    self: str | None


class GitLabProjectNamespaceTypedDict(TypedDict):
    id: int | None
    kind: str | None


class GitLabProjectTypedDict(TypedDict):
    _links: GitLabProjectLinksTypedDict | None
    avatar_url: str | None
    container_registry_image_prefix: str | None
    created_at: str | None
    default_branch: str | None
    description: str | None
    http_url_to_repo: str | None
    id: int
    last_activity_at: str | None
    name: str | None
    name_with_namespace: str | None
    namespace: GitLabProjectNamespaceTypedDict | None
    open_issues_count: int | None
    path: str | None
    path_with_namespace: str | None
    readme_url: str | None
    ssh_url_to_repo: str | None
    updated_at: str | None
    web_url: str | None


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
        git_lab_group: GitLabProject = GitLabProject.objects.get_or_create(id=project_id)[0]
        git_lab_group.avatar_url = project_dict.get("avatar_url")
        git_lab_group.container_registry_image_prefix = project_dict.get("container_registry_image_prefix")
        git_lab_group.created_at = project_dict.get("created_at")
        git_lab_group.default_branch = project_dict.get("default_branch")
        git_lab_group.description = project_dict.get("description")
        git_lab_group.http_url_to_repo = project_dict.get("http_url_to_repo")
        git_lab_group.last_activity_at = project_dict.get("last_activity_at")
        links: GitLabProjectLinksTypedDict | None = project_dict.get("_links")
        if links is not None:
            git_lab_group.link_cluster_agents = links.get("cluster_agents")
            git_lab_group.link_events = links.get("events")
            git_lab_group.link_issues = links.get("issues")
            git_lab_group.link_labels = links.get("labels")
            git_lab_group.link_members = links.get("members")
            git_lab_group.link_merge_requests = links.get("merge_requests")
            git_lab_group.link_repo_branches = links.get("repo_branches")
            git_lab_group.link_self = links.get("self")
        git_lab_group.name = project_dict.get("name")
        git_lab_group.name_with_namespace = project_dict.get("name_with_namespace")
        namespace: GitLabProjectNamespaceTypedDict | None = project_dict.get("namespace")
        if namespace is not None:
            namespace_id: int | None = namespace.get("id")
            namespace_kind: str | None = namespace.get("kind")
            if namespace_kind == "group":
                group: GitLabGroup | None = GitLabGroup.objects.filter(id=namespace_id).first()
                if group is not None:
                    git_lab_group.group = group
        git_lab_group.open_issues_count = project_dict.get("open_issues_count")
        git_lab_group.path = project_dict.get("path")
        git_lab_group.path_with_namespace = project_dict.get("path_with_namespace")
        git_lab_group.readme_url = project_dict.get("readme_url")
        git_lab_group.ssh_url_to_repo = project_dict.get("ssh_url_to_repo")
        git_lab_group.updated_at = project_dict.get("updated_at")
        git_lab_group.web_url = project_dict.get("web_url")
        git_lab_group.save()
    return JsonResponse(data=project_dicts, safe=False)
