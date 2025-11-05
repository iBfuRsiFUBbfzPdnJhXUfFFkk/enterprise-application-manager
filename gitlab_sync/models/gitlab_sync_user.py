from datetime import datetime

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from core.utilities.cast_query_set import cast_query_set
from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_datetime import create_generic_datetime
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_varchar import create_generic_varchar
from gitlab_sync.models.common.abstract import (
    AbstractGitLabAvatarUrl,
    AbstractGitLabCreatedAt,
    AbstractGitLabPrimaryKey,
    AbstractGitLabState,
    AbstractGitLabWebUrl,
)


class GitLabSyncUser(
    AbstractBaseModel,
    AbstractGitLabAvatarUrl,
    AbstractGitLabCreatedAt,
    AbstractGitLabPrimaryKey,
    AbstractGitLabState,
    AbstractGitLabWebUrl,
    AbstractName,
):
    """
    Represents a GitLab user synced from GitLab EE 17.11.6.

    Improved implementation with additional user metadata tracking.
    """

    expires_at: datetime | None = create_generic_datetime()
    locked: bool | None = create_generic_boolean()
    username: str | None = create_generic_varchar()
    email: str | None = create_generic_varchar()
    bot: bool | None = create_generic_boolean()
    person: "Person | None" = create_generic_fk(to="core.Person")

    @property
    def commits_authored(self):
        from gitlab_sync.models.gitlab_sync_commit import GitLabSyncCommit

        return cast_query_set(
            typ=GitLabSyncCommit, val=GitLabSyncCommit.objects.filter(author=self)
        )

    @property
    def issues_assigned(self):
        from gitlab_sync.models.gitlab_sync_issue import GitLabSyncIssue

        return cast_query_set(
            typ=GitLabSyncIssue, val=GitLabSyncIssue.objects.filter(assignees__in=[self])
        )

    @property
    def issues_authored(self):
        from gitlab_sync.models.gitlab_sync_issue import GitLabSyncIssue

        return cast_query_set(
            typ=GitLabSyncIssue, val=GitLabSyncIssue.objects.filter(author=self)
        )

    @property
    def merge_requests_assigned(self):
        from gitlab_sync.models.gitlab_sync_merge_request import GitLabSyncMergeRequest

        return cast_query_set(
            typ=GitLabSyncMergeRequest,
            val=GitLabSyncMergeRequest.objects.filter(assignees__in=[self]),
        )

    @property
    def merge_requests_authored(self):
        from gitlab_sync.models.gitlab_sync_merge_request import GitLabSyncMergeRequest

        return cast_query_set(
            typ=GitLabSyncMergeRequest,
            val=GitLabSyncMergeRequest.objects.filter(author=self),
        )

    @property
    def merge_requests_reviewed(self):
        from gitlab_sync.models.gitlab_sync_merge_request import GitLabSyncMergeRequest

        return cast_query_set(
            typ=GitLabSyncMergeRequest,
            val=GitLabSyncMergeRequest.objects.filter(reviewers__in=[self]),
        )

    @property
    def pipelines_triggered(self):
        from gitlab_sync.models.gitlab_sync_pipeline import GitLabSyncPipeline

        return cast_query_set(
            typ=GitLabSyncPipeline, val=GitLabSyncPipeline.objects.filter(user=self)
        )

    def __str__(self) -> str:
        return f"{self.username}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "GitLab Sync User"
        verbose_name_plural = "GitLab Sync Users"
