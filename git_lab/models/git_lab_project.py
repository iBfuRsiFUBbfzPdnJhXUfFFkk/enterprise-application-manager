from datetime import datetime

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from django_generic_model_fields.create_generic_datetime import create_generic_datetime
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_varchar import create_generic_varchar
from core.utilities.cast_query_set import cast_query_set
from git_lab.models.common.abstract.abstract_git_lab_avatar_url import AbstractGitLabAvatarUrl
from git_lab.models.common.abstract.abstract_git_lab_created_at import AbstractGitLabCreatedAt
from git_lab.models.common.abstract.abstract_git_lab_description import AbstractGitLabDescription
from git_lab.models.common.abstract.abstract_git_lab_path import AbstractGitLabPath
from git_lab.models.common.abstract.abstract_git_lab_primary_key import AbstractGitLabPrimaryKey
from git_lab.models.common.abstract.abstract_git_lab_updated_at import AbstractGitLabUpdatedAt
from git_lab.models.common.abstract.abstract_git_lab_web_url import AbstractGitLabWebUrl
from git_lab.models.git_lab_group import GitLabGroup


class GitLabProject(
    AbstractBaseModel,
    AbstractGitLabAvatarUrl,
    AbstractGitLabCreatedAt,
    AbstractGitLabDescription,
    AbstractGitLabPath,
    AbstractGitLabPrimaryKey,
    AbstractGitLabUpdatedAt,
    AbstractGitLabWebUrl,
    AbstractName,
):
    container_registry_image_prefix: str | None = create_generic_varchar()
    default_branch: str | None = create_generic_varchar()
    group: GitLabGroup | None = create_generic_fk(related_name="projects", to=GitLabGroup)
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
    path_with_namespace: str | None = create_generic_varchar()
    readme_url: str | None = create_generic_varchar()
    ssh_url_to_repo: str | None = create_generic_varchar()

    @property
    def changes(self):
        from git_lab.models.git_lab_change import GitLabChange
        return cast_query_set(
            typ=GitLabChange,
            val=GitLabChange.objects.filter(project=self)
        )

    @property
    def issues(self):
        from git_lab.models.git_lab_issue import GitLabIssue
        return cast_query_set(
            typ=GitLabIssue,
            val=GitLabIssue.objects.filter(project=self)
        )

    @property
    def merge_requests(self):
        from git_lab.models.git_lab_merge_request import GitLabMergeRequest
        return cast_query_set(
            typ=GitLabMergeRequest,
            val=GitLabMergeRequest.objects.filter(project=self)
        )

    def __str__(self) -> str:
        return f"{self.path_with_namespace}"

    class Meta:
        ordering = ['path_with_namespace']
        verbose_name = "GitLab Project"
        verbose_name_plural = "GitLab Projects"
