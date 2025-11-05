from datetime import datetime

from django.http import HttpRequest, JsonResponse

from gitlab_sync.models import GitLabSyncJobTracker


def gitlab_sync_cancel_job_api(request: HttpRequest, job_id: int) -> JsonResponse:
    """
    Cancel a running sync job.

    Marks the job as cancelled. Note: This won't stop the actual thread
    execution immediately, but the job status will be marked as cancelled
    and polling will stop on the frontend.

    Args:
        request: HTTP request
        job_id: ID of the job to cancel

    Returns:
        JSON with success status
    """
    if request.method != "POST":
        return JsonResponse(
            data={"success": False, "error": "Method not allowed"}, status=405
        )

    job_tracker = GitLabSyncJobTracker.objects.filter(id=job_id).first()

    if not job_tracker:
        return JsonResponse(
            data={"success": False, "error": "Job not found"}, status=404
        )

    if job_tracker.status != "running":
        return JsonResponse(
            data={
                "success": False,
                "error": f"Job is not running (status: {job_tracker.status})",
            },
            status=400,
        )

    # Mark as cancelled
    job_tracker.status = "cancelled"
    job_tracker.end_time = datetime.now()

    # Add cancellation log
    if not job_tracker.detailed_logs:
        job_tracker.detailed_logs = []
    job_tracker.detailed_logs.append(
        f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️ Job cancelled by user"
    )

    job_tracker.save()

    return JsonResponse(
        data={
            "success": True,
            "message": "Job cancelled successfully",
            "job_id": job_id,
        }
    )
