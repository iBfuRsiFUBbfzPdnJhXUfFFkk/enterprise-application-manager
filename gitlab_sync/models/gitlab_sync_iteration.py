from datetime import date, datetime

from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_name import AbstractName
from core.utilities.cast_query_set import cast_query_set
from gitlab_sync.models.common.abstract import AbstractGitLabWebUrl


class GitLabSyncIteration(
    AbstractBaseModel,
    AbstractGitLabWebUrl,
    AbstractName,
):
    """
    Represents an iteration (group-level sprint) synced from GitLab EE 17.11.6.

    Iterations are used for agile planning and tracking work over time periods.
    """

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    group = models.ForeignKey(
        "gitlab_sync.GitLabSyncGroup",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="iterations",
    )
    gitlab_id: int | None = models.IntegerField(null=True, blank=True)
    title: str | None = models.CharField(max_length=255, null=True, blank=True)
    description: str | None = models.CharField(max_length=255, null=True, blank=True)
    state: str | None = models.CharField(
        max_length=255,
        choices=[
            ("upcoming", "Upcoming"),
            ("started", "Started"),
            ("closed", "Closed"),
        ],
        null=True,
        blank=True,
    )
    due_date: date | None = models.DateField(null=True, blank=True)
    start_date: date | None = models.DateField(null=True, blank=True)
    sequence: int | None = models.IntegerField(null=True, blank=True)
    created_at: datetime | None = models.DateTimeField(null=True, blank=True)
    updated_at: datetime | None = models.DateTimeField(null=True, blank=True)

    @property
    def issues(self):
        from gitlab_sync.models.gitlab_sync_issue import GitLabSyncIssue

        return cast_query_set(
            typ=GitLabSyncIssue, val=GitLabSyncIssue.objects.filter(iteration=self)
        )

    @property
    def merge_requests(self):
        from gitlab_sync.models.gitlab_sync_merge_request import GitLabSyncMergeRequest

        return cast_query_set(
            typ=GitLabSyncMergeRequest,
            val=GitLabSyncMergeRequest.objects.filter(iteration=self),
        )

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        ordering = ["-start_date", "-sequence"]
        verbose_name = "GitLab Sync Iteration"
        verbose_name_plural = "GitLab Sync Iterations"
