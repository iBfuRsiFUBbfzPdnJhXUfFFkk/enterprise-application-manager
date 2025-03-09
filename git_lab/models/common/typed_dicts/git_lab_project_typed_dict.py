from typing import TypedDict

from git_lab.models.common.typed_dicts.git_lab_links_typed_dict import GitLabLinksTypedDict
from git_lab.models.common.typed_dicts.git_lab_namespace_typed_dict import GitLabNamespaceTypedDict


class GitLabProjectTypedDict(TypedDict):
    _links: GitLabLinksTypedDict | None
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
    namespace: GitLabNamespaceTypedDict | None
    open_issues_count: int | None
    path: str | None
    path_with_namespace: str | None
    readme_url: str | None
    ssh_url_to_repo: str | None
    updated_at: str | None
    web_url: str | None