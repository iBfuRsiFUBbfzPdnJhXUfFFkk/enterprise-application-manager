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
    AbstractGitLabState,
    AbstractGitLabTitle,
    AbstractGitLabUpdatedAt,
    AbstractGitLabWebUrl,
)


class GitLabSyncEpic(
    AbstractBaseModel,
    AbstractGitLabClosedAt,
    AbstractGitLabCreatedAt,
    AbstractGitLabDescription,
    AbstractGitLabInternalIdentification,
    AbstractGitLabPrimaryKey,
    AbstractGitLabState,
    AbstractGitLabTitle,
    AbstractGitLabUpdatedAt,
    AbstractGitLabWebUrl,
):
    """
    Represents a GitLab Epic (Enterprise Edition feature) from GitLab EE 17.11.6.

    Epics are high-level organizational items that group related issues.
    Only available in GitLab Enterprise Edition.
    """

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    group = models.ForeignKey(
        "gitlab_sync.GitLabSyncGroup",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="epics",
    )
    author = models.ForeignKey(
        "gitlab_sync.GitLabSyncUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="epics_authored",
    )
    parent_epic = models.ForeignKey(
        "gitlab_sync.GitLabSyncEpic",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="child_epics",
    )
    # labels field removed - core.Label model doesn't exist
    # can be added later if needed
    start_date: datetime | None = models.DateTimeField(null=True, blank=True)
    end_date: datetime | None = models.DateTimeField(null=True, blank=True)
    start_date_is_fixed: bool | None = models.BooleanField(null=True, blank=True)
    start_date_fixed: datetime | None = models.DateTimeField(null=True, blank=True)
    start_date_from_inherited_source: datetime | None = models.DateTimeField(null=True, blank=True)
    due_date: datetime | None = models.DateTimeField(null=True, blank=True)
    due_date_is_fixed: bool | None = models.BooleanField(null=True, blank=True)
    due_date_fixed: datetime | None = models.DateTimeField(null=True, blank=True)
    due_date_from_inherited_source: datetime | None = models.DateTimeField(null=True, blank=True)
    upvotes: int | None = models.IntegerField(null=True, blank=True)
    downvotes: int | None = models.IntegerField(null=True, blank=True)
    user_notes_count: int | None = models.IntegerField(null=True, blank=True)
    confidential: bool | None = models.BooleanField(null=True, blank=True)
    color: str | None = models.CharField(max_length=255, null=True, blank=True)

    @property
    def issues(self):
        from gitlab_sync.models.gitlab_sync_issue import GitLabSyncIssue

        return cast_query_set(
            typ=GitLabSyncIssue, val=GitLabSyncIssue.objects.filter(epic=self)
        )

    def __str__(self) -> str:
        return f"Epic &{self.iid}: {self.title}"

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "GitLab Sync Epic"
        verbose_name_plural = "GitLab Sync Epics"
