from dataclasses import dataclass, field
from datetime import datetime

from django.utils import timezone


@dataclass
class SyncResult:
    """
    Tracks the result of a GitLab entity sync operation.

    Provides detailed statistics about the sync process including
    success/failure counts, error messages, and real-time progress updates.
    """

    entity_type: str
    success: bool = True
    synced_count: int = 0
    failed_count: int = 0
    skipped_count: int = 0
    errors: list[str] = field(default_factory=list)
    logs: list[str] = field(default_factory=list)
    start_time: datetime = field(default_factory=timezone.now)
    end_time: datetime | None = None
    job_tracker_id: int | None = None
    current_count: int = 0
    estimated_total: int = 0

    def add_success(self) -> None:
        """Increment successful sync count."""
        self.synced_count += 1

    def add_failure(self, error_message: str) -> None:
        """Add a failure with error message."""
        self.failed_count += 1
        self.errors.append(error_message)
        if self.failed_count > 0:
            self.success = False

    def add_skip(self) -> None:
        """Increment skipped entity count."""
        self.skipped_count += 1

    def finish(self) -> None:
        """Mark sync as finished and record end time."""
        self.end_time = timezone.now()
        self._update_job_tracker()

    def add_log(self, message: str) -> None:
        """Add a log message and update job tracker."""
        timestamp = timezone.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.logs.append(log_entry)
        self._update_job_tracker()

    def update_progress(
        self, current: int, total: int, message: str | None = None
    ) -> None:
        """Update progress tracking and job tracker."""
        self.current_count = current
        self.estimated_total = total
        if message:
            self.add_log(message)
        else:
            self._update_job_tracker()

    def _update_job_tracker(self) -> None:
        """Update the database job tracker with current progress."""
        if not self.job_tracker_id:
            return

        try:
            from gitlab_sync.models import GitLabSyncJobTracker

            job_tracker = GitLabSyncJobTracker.objects.filter(
                id=self.job_tracker_id
            ).first()
            if not job_tracker:
                error_msg = f"Job tracker {self.job_tracker_id} not found!"
                print(f"[SyncResult] {error_msg}")
                self.logs.append(f"[{timezone.now().strftime('%H:%M:%S')}] ❌ {error_msg}")
                return

            job_tracker.current_count = self.current_count
            job_tracker.total_count = self.estimated_total
            job_tracker.progress_percent = self._calculate_progress_percent()
            job_tracker.error_messages = self.errors
            job_tracker.detailed_logs = self.logs
            job_tracker.end_time = self.end_time

            if self.end_time:
                job_tracker.status = "failed" if not self.success else "completed"

            job_tracker.save()
            print(
                f"[SyncResult] Updated job {self.job_tracker_id}: {self.current_count}/{self.estimated_total} ({self._calculate_progress_percent()}%)"
            )
        except Exception as e:
            error_msg = f"Error updating job tracker: {e}"
            print(f"[SyncResult] {error_msg}")
            import traceback
            traceback.print_exc()

            # Add error to logs so it's visible if we can update later
            timestamp = timezone.now().strftime("%H:%M:%S")
            self.logs.append(f"[{timestamp}] ❌ Database update error: {str(e)}")
            self.errors.append(f"Job tracker update failed: {str(e)}")
            self.success = False

    def _calculate_progress_percent(self) -> int:
        """Calculate progress as a percentage (0-100)."""
        if self.estimated_total == 0:
            return 0
        percent = int((self.current_count / self.estimated_total) * 100)
        return min(percent, 100)

    @property
    def duration_seconds(self) -> float:
        """Calculate sync duration in seconds."""
        if self.end_time is None:
            return 0.0
        return (self.end_time - self.start_time).total_seconds()

    @property
    def total_processed(self) -> int:
        """Total entities processed (synced + failed + skipped)."""
        return self.synced_count + self.failed_count + self.skipped_count

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "entity_type": self.entity_type,
            "success": self.success,
            "synced_count": self.synced_count,
            "failed_count": self.failed_count,
            "skipped_count": self.skipped_count,
            "total_processed": self.total_processed,
            "duration_seconds": self.duration_seconds,
            "errors": self.errors,
            "logs": self.logs,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "job_tracker_id": self.job_tracker_id,
            "current_count": self.current_count,
            "estimated_total": self.estimated_total,
            "progress_percent": self._calculate_progress_percent(),
        }

    def __str__(self) -> str:
        """String representation of sync result."""
        return (
            f"{self.entity_type} Sync: "
            f"{self.synced_count} synced, "
            f"{self.failed_count} failed, "
            f"{self.skipped_count} skipped "
            f"({self.duration_seconds:.2f}s)"
        )
