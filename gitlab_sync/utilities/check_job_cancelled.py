from gitlab_sync.models import GitLabSyncJobTracker


def check_job_cancelled(job_tracker_id: int | None) -> bool:
    """
    Check if a job has been cancelled.

    This allows sync operations to detect cancellation and exit early
    instead of continuing to process data.

    Args:
        job_tracker_id: ID of the job tracker to check

    Returns:
        True if job was cancelled, False otherwise
    """
    if not job_tracker_id:
        return False

    try:
        job_tracker = GitLabSyncJobTracker.objects.filter(id=job_tracker_id).first()
        if not job_tracker:
            return False

        return job_tracker.status == "cancelled"
    except Exception:
        # If we can't check, assume not cancelled
        return False
