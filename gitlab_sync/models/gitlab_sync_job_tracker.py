from datetime import datetime

from django.db import models
from django.db.models import JSONField, QuerySet

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.enums.gitlab_sync_job_status_choices import (
    GITLAB_SYNC_JOB_STATUS_CHOICES,
)
from core.models.common.enums.gitlab_sync_job_type_choices import (
    GITLAB_SYNC_JOB_TYPE_CHOICES,
)
from core.utilities.cast_query_set import cast_query_set


class GitLabSyncJobTracker(AbstractBaseModel):
    """
    Tracks long-running GitLab sync operations for progress monitoring.

    Allows users to monitor sync progress in real-time or navigate away
    and check back later without using Celery or external task queues.
    """

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    job_type: str | None = models.CharField(
        max_length=255, choices=GITLAB_SYNC_JOB_TYPE_CHOICES, null=True, blank=True
    )
    status: str | None = models.CharField(
        max_length=255, choices=GITLAB_SYNC_JOB_STATUS_CHOICES, null=True, blank=True
    )
    progress_percent: int | None = models.IntegerField(null=True, blank=True)
    current_count: int | None = models.IntegerField(null=True, blank=True)
    total_count: int | None = models.IntegerField(null=True, blank=True)
    start_time: datetime | None = models.DateTimeField(null=True, blank=True)
    end_time: datetime | None = models.DateTimeField(null=True, blank=True)
    error_messages: list[str] = JSONField(default=list, blank=True)
    detailed_logs: list[str] = JSONField(default=list, blank=True)
    user: "User | None" = models.ForeignKey(
        "core.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="gitlab_sync_job_trackers"
    )

    @property
    def duration_seconds(self) -> float | None:
        """Calculate duration in seconds."""
        if not self.start_time:
            return None
        end = self.end_time or datetime.now(self.start_time.tzinfo)
        return (end - self.start_time).total_seconds()

    @property
    def is_running(self) -> bool:
        """Check if job is currently running."""
        return self.status == "running"

    @property
    def is_completed(self) -> bool:
        """Check if job completed successfully."""
        return self.status == "completed"

    @property
    def is_failed(self) -> bool:
        """Check if job failed."""
        return self.status == "failed"

    @property
    def is_cancelled(self) -> bool:
        """Check if job was cancelled."""
        return self.status == "cancelled"

    @staticmethod
    def get_running_jobs() -> QuerySet["GitLabSyncJobTracker"]:
        """Get all currently running jobs."""
        return cast_query_set(
            typ=GitLabSyncJobTracker,
            val=GitLabSyncJobTracker.objects.filter(status="running"),
        )

    @staticmethod
    def get_user_running_jobs(user) -> QuerySet["GitLabSyncJobTracker"]:
        """Get all currently running jobs for a specific user."""
        return cast_query_set(
            typ=GitLabSyncJobTracker,
            val=GitLabSyncJobTracker.objects.filter(status="running", user=user),
        )

    def __str__(self) -> str:
        return f"{self.job_type} - {self.status} ({self.progress_percent}%)"

    class Meta:
        ordering = ["-start_time"]
        verbose_name = "GitLab Sync Job Tracker"
        verbose_name_plural = "GitLab Sync Job Trackers"
