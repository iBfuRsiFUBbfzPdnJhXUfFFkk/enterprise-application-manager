from django.http import HttpRequest, JsonResponse

from gitlab_sync.models import GitLabSyncJobTracker


def gitlab_sync_job_status_api(request: HttpRequest, job_id: int) -> JsonResponse:
    """
    Get the current status of a sync job.

    Polled by frontend to display real-time progress updates.

    Args:
        request: HTTP request
        job_id: ID of the job tracker to query

    Returns:
        JSON with job status, progress, logs, etc.
    """
    job_tracker = GitLabSyncJobTracker.objects.filter(id=job_id).first()

    if not job_tracker:
        return JsonResponse(data={"success": False, "error": "Job not found"}, status=404)

    return JsonResponse(
        data={
            "success": True,
            "job_id": job_tracker.id,
            "job_type": job_tracker.job_type,
            "status": job_tracker.status,
            "progress_percent": job_tracker.progress_percent or 0,
            "current_count": job_tracker.current_count or 0,
            "total_count": job_tracker.total_count or 0,
            "start_time": (
                job_tracker.start_time.isoformat() if job_tracker.start_time else None
            ),
            "end_time": (
                job_tracker.end_time.isoformat() if job_tracker.end_time else None
            ),
            "duration_seconds": job_tracker.duration_seconds,
            "error_messages": job_tracker.error_messages or [],
            "detailed_logs": job_tracker.detailed_logs or [],
            "is_running": job_tracker.is_running,
            "is_completed": job_tracker.is_completed,
            "is_failed": job_tracker.is_failed,
            "is_cancelled": job_tracker.is_cancelled,
            "user_username": job_tracker.user.username if job_tracker.user else None,
        }
    )
