from datetime import datetime

from django.db.models import JSONField, QuerySet

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.enums.gitlab_sync_job_status_choices import (
    GITLAB_SYNC_JOB_STATUS_CHOICES,
)
from core.models.common.enums.gitlab_sync_job_type_choices import (
    GITLAB_SYNC_JOB_TYPE_CHOICES,
)
from core.utilities.cast_query_set import cast_query_set
from django_generic_model_fields.create_generic_datetime import create_generic_datetime
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer


class GitLabSyncJobTracker(AbstractBaseModel):
    """
    Tracks long-running GitLab sync operations for progress monitoring.

    Allows users to monitor sync progress in real-time or navigate away
    and check back later without using Celery or external task queues.
    """

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    job_type: str | None = create_generic_enum(choices=GITLAB_SYNC_JOB_TYPE_CHOICES)
    status: str | None = create_generic_enum(choices=GITLAB_SYNC_JOB_STATUS_CHOICES)
    progress_percent: int | None = create_generic_integer()
    current_count: int | None = create_generic_integer()
    total_count: int | None = create_generic_integer()
    start_time: datetime | None = create_generic_datetime()
    end_time: datetime | None = create_generic_datetime()
    error_messages: list[str] = JSONField(default=list, blank=True)
    detailed_logs: list[str] = JSONField(default=list, blank=True)
    user: "User | None" = create_generic_fk(to="core.User")

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
