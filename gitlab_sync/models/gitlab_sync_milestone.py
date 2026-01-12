from datetime import date, datetime

from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from core.utilities.cast_query_set import cast_query_set
from gitlab_sync.models.common.abstract import AbstractGitLabWebUrl


class GitLabSyncMilestone(
    AbstractBaseModel,
    AbstractGitLabWebUrl,
    AbstractName,
):
    """
    Represents a milestone (project or group) synced from GitLab EE 17.11.6.

    Milestones are used to track issues and merge requests over a period of time.
    """

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    project = models.ForeignKey(
        "gitlab_sync.GitLabSyncProject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="milestones",
    )
    group = models.ForeignKey(
        "gitlab_sync.GitLabSyncGroup",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="milestones",
    )
    gitlab_id: int | None = models.IntegerField(null=True, blank=True)
    title: str | None = models.CharField(max_length=255, null=True, blank=True)
    description: str | None = models.CharField(max_length=255, null=True, blank=True)
    state: str | None = models.CharField(
        max_length=255,
        choices=[
            ("active", "Active"),
            ("closed", "Closed"),
        ],
        null=True,
        blank=True,
    )
    due_date: date | None = models.DateField(null=True, blank=True)
    start_date: date | None = models.DateField(null=True, blank=True)
    created_at: datetime | None = models.DateTimeField(null=True, blank=True)
    updated_at: datetime | None = models.DateTimeField(null=True, blank=True)

    @property
    def issues(self):
        from gitlab_sync.models.gitlab_sync_issue import GitLabSyncIssue

        return cast_query_set(
            typ=GitLabSyncIssue, val=GitLabSyncIssue.objects.filter(milestone=self)
        )

    @property
    def merge_requests(self):
        from gitlab_sync.models.gitlab_sync_merge_request import GitLabSyncMergeRequest

        return cast_query_set(
            typ=GitLabSyncMergeRequest,
            val=GitLabSyncMergeRequest.objects.filter(milestone=self),
        )

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        ordering = ["-due_date", "-created_at"]
        verbose_name = "GitLab Sync Milestone"
        verbose_name_plural = "GitLab Sync Milestones"
