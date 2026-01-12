from datetime import datetime

from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.utilities.cast_query_set import cast_query_set
from gitlab_sync.models.common.abstract import (
    AbstractGitLabClosedAt,
    AbstractGitLabCreatedAt,
    AbstractGitLabDescription,
    AbstractGitLabInternalIdentification,
    AbstractGitLabPrimaryKey,
    AbstractGitLabReferences,
    AbstractGitLabState,
    AbstractGitLabTaskCompletionStatus,
    AbstractGitLabTimeStats,
    AbstractGitLabTitle,
    AbstractGitLabUpdatedAt,
    AbstractGitLabWebUrl,
)


class GitLabSyncMergeRequest(
    AbstractBaseModel,
    AbstractGitLabClosedAt,
    AbstractGitLabCreatedAt,
    AbstractGitLabDescription,
    AbstractGitLabInternalIdentification,
    AbstractGitLabPrimaryKey,
    AbstractGitLabReferences,
    AbstractGitLabState,
    AbstractGitLabTaskCompletionStatus,
    AbstractGitLabTimeStats,
    AbstractGitLabTitle,
    AbstractGitLabUpdatedAt,
    AbstractGitLabWebUrl,
):
    """
    Represents a GitLab merge request synced from GitLab EE 17.11.6.

    Improved implementation with enhanced pipeline and code review tracking.
    """

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    assignees = models.ManyToManyField(
        "gitlab_sync.GitLabSyncUser",
        blank=True,
        related_name="merge_requests_assigned",
    )
    author = models.ForeignKey(
        "gitlab_sync.GitLabSyncUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="merge_requests_authored",
    )
    closed_by = models.ForeignKey(
        "gitlab_sync.GitLabSyncUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="merge_requests_closed",
    )
    merged_by = models.ForeignKey(
        "gitlab_sync.GitLabSyncUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="merge_requests_merged",
    )
    reviewers = models.ManyToManyField(
        "gitlab_sync.GitLabSyncUser",
        blank=True,
        related_name="merge_requests_reviewed",
    )
    group = models.ForeignKey(
        "gitlab_sync.GitLabSyncGroup",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="merge_requests",
    )
    project = models.ForeignKey(
        "gitlab_sync.GitLabSyncProject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="merge_requests",
    )
    head_pipeline = models.ForeignKey(
        "gitlab_sync.GitLabSyncPipeline",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="merge_requests",
    )
    milestone = models.ForeignKey(
        "gitlab_sync.GitLabSyncMilestone",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="merge_requests",
    )
    iteration = models.ForeignKey(
        "gitlab_sync.GitLabSyncIteration",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="merge_requests",
    )
    blocking_discussions_resolved: bool | None = models.BooleanField(null=True, blank=True)
    draft: bool | None = models.BooleanField(null=True, blank=True)
    has_conflicts: bool | None = models.BooleanField(null=True, blank=True)
    merged_at: datetime | None = models.DateTimeField(null=True, blank=True)
    prepared_at: datetime | None = models.DateTimeField(null=True, blank=True)
    sha: str | None = models.CharField(max_length=255, null=True, blank=True)
    source_branch: str | None = models.CharField(max_length=255, null=True, blank=True)
    target_branch: str | None = models.CharField(max_length=255, null=True, blank=True)
    squash: bool | None = models.BooleanField(null=True, blank=True)
    squash_commit_sha: str | None = models.CharField(max_length=255, null=True, blank=True)
    merge_status: str | None = models.CharField(max_length=255, null=True, blank=True)
    diff_refs_base_sha: str | None = models.CharField(max_length=255, null=True, blank=True)
    diff_refs_head_sha: str | None = models.CharField(max_length=255, null=True, blank=True)
    diff_refs_start_sha: str | None = models.CharField(max_length=255, null=True, blank=True)
    user_notes_count: int | None = models.IntegerField(null=True, blank=True)
    upvotes: int | None = models.IntegerField(null=True, blank=True)
    downvotes: int | None = models.IntegerField(null=True, blank=True)

    @property
    def pipelines(self):
        from gitlab_sync.models.gitlab_sync_pipeline import GitLabSyncPipeline

        return cast_query_set(
            typ=GitLabSyncPipeline,
            val=GitLabSyncPipeline.objects.filter(merge_request=self),
        )

    def __str__(self) -> str:
        return f"!{self.iid}: {self.title}"

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "GitLab Sync Merge Request"
        verbose_name_plural = "GitLab Sync Merge Requests"
