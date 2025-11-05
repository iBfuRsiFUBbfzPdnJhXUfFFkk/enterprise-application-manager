from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SyncResult:
    """
    Tracks the result of a GitLab entity sync operation.

    Provides detailed statistics about the sync process including
    success/failure counts and error messages.
    """

    entity_type: str
    success: bool = True
    synced_count: int = 0
    failed_count: int = 0
    skipped_count: int = 0
    errors: list[str] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: datetime | None = None

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
        self.end_time = datetime.now()

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
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
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
