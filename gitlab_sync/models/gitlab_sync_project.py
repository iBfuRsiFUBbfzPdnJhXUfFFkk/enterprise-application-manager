from datetime import datetime

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from core.utilities.cast_query_set import cast_query_set
from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_datetime import create_generic_datetime
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_varchar import create_generic_varchar
from gitlab_sync.models.common.abstract import (
    AbstractGitLabAvatarUrl,
    AbstractGitLabCreatedAt,
    AbstractGitLabDescription,
    AbstractGitLabPath,
    AbstractGitLabPrimaryKey,
    AbstractGitLabUpdatedAt,
    AbstractGitLabWebUrl,
)


class GitLabSyncProject(
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
    """
    Represents a GitLab project synced from GitLab EE 17.11.6.

    Improved implementation with enhanced repository tracking capabilities.
    """

    container_registry_image_prefix: str | None = create_generic_varchar()
    default_branch: str | None = create_generic_varchar()
    group = create_generic_fk(
        related_name="projects",
        to="gitlab_sync.GitLabSyncGroup",
    )
    http_url_to_repo: str | None = create_generic_varchar()
    last_activity_at: datetime | None = create_generic_datetime()
    name_with_namespace: str | None = create_generic_varchar()
    open_issues_count: int | None = create_generic_integer()
    path_with_namespace: str | None = create_generic_varchar()
    readme_url: str | None = create_generic_varchar()
    ssh_url_to_repo: str | None = create_generic_varchar()
    visibility: str | None = create_generic_varchar()
    archived: bool | None = create_generic_boolean()
    star_count: int | None = create_generic_integer()
    forks_count: int | None = create_generic_integer()

    @property
    def repository(self):
        from gitlab_sync.models.gitlab_sync_repository import GitLabSyncRepository

        return GitLabSyncRepository.objects.filter(project=self).first()

    @property
    def commits(self):
        from gitlab_sync.models.gitlab_sync_commit import GitLabSyncCommit

        return cast_query_set(
            typ=GitLabSyncCommit, val=GitLabSyncCommit.objects.filter(project=self)
        )

    @property
    def branches(self):
        from gitlab_sync.models.gitlab_sync_branch import GitLabSyncBranch

        return cast_query_set(
            typ=GitLabSyncBranch, val=GitLabSyncBranch.objects.filter(project=self)
        )

    @property
    def pipelines(self):
        from gitlab_sync.models.gitlab_sync_pipeline import GitLabSyncPipeline

        return cast_query_set(
            typ=GitLabSyncPipeline, val=GitLabSyncPipeline.objects.filter(project=self)
        )

    @property
    def issues(self):
        from gitlab_sync.models.gitlab_sync_issue import GitLabSyncIssue

        return cast_query_set(
            typ=GitLabSyncIssue, val=GitLabSyncIssue.objects.filter(project=self)
        )

    @property
    def merge_requests(self):
        from gitlab_sync.models.gitlab_sync_merge_request import GitLabSyncMergeRequest

        return cast_query_set(
            typ=GitLabSyncMergeRequest,
            val=GitLabSyncMergeRequest.objects.filter(project=self),
        )

    def __str__(self) -> str:
        return f"{self.path_with_namespace}"

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "GitLab Sync Project"
        verbose_name_plural = "GitLab Sync Projects"
