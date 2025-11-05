from datetime import timedelta

from django.utils import timezone

from gitlab_sync.models import GitLabSyncJobTracker


def cleanup_stale_jobs(max_runtime_minutes: int = 60) -> int:
    """
    Clean up stale jobs that have been running too long.

    Jobs that are marked as "running" but haven't been updated in X minutes
    are likely orphaned by a server restart or thread crash. Mark them as failed.

    Args:
        max_runtime_minutes: Maximum runtime before considering a job stale (default: 60 minutes)

    Returns:
        Number of jobs cleaned up
    """
    cutoff_time = timezone.now() - timedelta(minutes=max_runtime_minutes)

    # Find jobs that are still "running" but started more than max_runtime_minutes ago
    stale_jobs = GitLabSyncJobTracker.objects.filter(
        status="running", start_time__lt=cutoff_time
    )

    count = 0
    for job in stale_jobs:
        # Mark as failed with explanation
        job.status = "failed"
        job.end_time = timezone.now()

        if not job.error_messages:
            job.error_messages = []
        job.error_messages.append(
            f"Job marked as stale - exceeded {max_runtime_minutes} minute runtime limit. "
            "Likely orphaned by server restart or thread crash."
        )

        if not job.detailed_logs:
            job.detailed_logs = []
        job.detailed_logs.append(
            f"[{timezone.now().strftime('%H:%M:%S')}] ⚠️ Job automatically marked as failed - exceeded runtime limit"
        )

        job.save()
        count += 1

        print(
            f"[CleanupStaleJobs] Marked job {job.id} ({job.job_type}) as failed - started {job.start_time}"
        )

    if count > 0:
        print(f"[CleanupStaleJobs] Cleaned up {count} stale jobs")

    return count
