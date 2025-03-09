from datetime import datetime

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.field_factories.create_generic_datetime import create_generic_datetime
from core.models.common.field_factories.create_generic_fk import create_generic_fk
from core.models.common.field_factories.create_generic_integer import create_generic_integer
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar
from git_lab.models.common.abstract.abstract_git_lab_primary_key import AbstractGitLabPrimaryKey
from git_lab.models.common.abstract.abstract_git_lab_web_url import AbstractGitLabWebUrl
from git_lab.models.git_lab_group import GitLabGroup


class GitLabProject(
    AbstractBaseModel,
    AbstractGitLabPrimaryKey,
    AbstractGitLabWebUrl,
    AbstractName,
):
    avatar_url: str | None = create_generic_varchar()
    container_registry_image_prefix: str | None = create_generic_varchar()
    created_at: datetime | None = create_generic_datetime()
    default_branch: str | None = create_generic_varchar()
    description: str | None = create_generic_varchar()
    group: GitLabGroup | None = create_generic_fk(to=GitLabGroup)
    http_url_to_repo: str | None = create_generic_varchar()
    last_activity_at: datetime | None = create_generic_datetime()
    link_cluster_agents: str | None = create_generic_varchar()
    link_events: str | None = create_generic_varchar()
    link_issues: str | None = create_generic_varchar()
    link_labels: str | None = create_generic_varchar()
    link_members: str | None = create_generic_varchar()
    link_merge_requests: str | None = create_generic_varchar()
    link_repo_branches: str | None = create_generic_varchar()
    link_self: str | None = create_generic_varchar()
    name_with_namespace: str | None = create_generic_varchar()
    open_issues_count: int | None = create_generic_integer()
    path: str | None = create_generic_varchar()
    path_with_namespace: str | None = create_generic_varchar()
    readme_url: str | None = create_generic_varchar()
    ssh_url_to_repo: str | None = create_generic_varchar()
    updated_at: datetime | None = create_generic_datetime()

    def __str__(self) -> str:
        return f"{self.path_with_namespace}"

    class Meta:
        ordering = ['path_with_namespace']
        verbose_name = "GitLab Project"
        verbose_name_plural = "GitLab Projects"
