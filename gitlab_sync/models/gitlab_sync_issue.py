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


class GitLabSyncIssue(
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
    Represents a GitLab issue synced from GitLab EE 17.11.6.

    Improved implementation with better tracking and validation.
    """

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    assignees = models.ManyToManyField(
        "gitlab_sync.GitLabSyncUser",
        blank=True,
        related_name="issues_assigned",
    )
    author = models.ForeignKey(
        "gitlab_sync.GitLabSyncUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issues_authored",
    )
    closed_by = models.ForeignKey(
        "gitlab_sync.GitLabSyncUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issues_closed",
    )
    group = models.ForeignKey(
        "gitlab_sync.GitLabSyncGroup",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issues",
    )
    project = models.ForeignKey(
        "gitlab_sync.GitLabSyncProject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issues",
    )
    epic = models.ForeignKey(
        "gitlab_sync.GitLabSyncEpic",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issues",
    )
    milestone = models.ForeignKey(
        "gitlab_sync.GitLabSyncMilestone",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issues",
    )
    iteration = models.ForeignKey(
        "gitlab_sync.GitLabSyncIteration",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="issues",
    )
    blocking_issues_count: int | None = models.IntegerField(null=True, blank=True)
    has_tasks: bool | None = models.BooleanField(null=True, blank=True)
    issue_type: str | None = models.CharField(max_length=255, null=True, blank=True)
    type: str | None = models.CharField(max_length=255, null=True, blank=True)
    user_notes_count: int | None = models.IntegerField(null=True, blank=True)
    weight: int | None = models.IntegerField(null=True, blank=True)
    severity: str | None = models.CharField(max_length=255, null=True, blank=True)
    due_date: str | None = models.CharField(max_length=255, null=True, blank=True)
    confidential: bool | None = models.BooleanField(null=True, blank=True)

    def __str__(self) -> str:
        return f"#{self.iid}: {self.title}"

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "GitLab Sync Issue"
        verbose_name_plural = "GitLab Sync Issues"
