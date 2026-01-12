from datetime import datetime

from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from core.utilities.cast_query_set import cast_query_set
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

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    expires_at: datetime | None = models.DateTimeField(null=True, blank=True)
    last_synced_at: datetime | None = models.DateTimeField(null=True, blank=True)
    locked: bool | None = models.BooleanField(null=True, blank=True)
    username: str | None = models.CharField(max_length=255, null=True, blank=True)
    email: str | None = models.CharField(max_length=255, null=True, blank=True)
    bot: bool | None = models.BooleanField(null=True, blank=True)
    person: "Person | None" = models.ForeignKey(
        "core.Person", on_delete=models.SET_NULL, null=True, blank=True, related_name="gitlab_sync_users"
    )

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
