import threading
from typing import Callable

from django.http import HttpRequest

from gitlab_sync.models import GitLabSyncJobTracker


def run_sync_in_background(
    job_type: str,
    sync_function: Callable[[HttpRequest, GitLabSyncJobTracker], None],
    request: HttpRequest,
) -> GitLabSyncJobTracker:
    """
    Run a sync operation in a background thread with job tracking.

    Args:
        job_type: Type of sync job (groups/projects/pipelines)
        sync_function: The actual sync function to execute
        request: Django HTTP request object

    Returns:
        GitLabSyncJobTracker: The created job tracker instance
    """
    from datetime import datetime

    job_tracker = GitLabSyncJobTracker.objects.create(
        job_type=job_type,
        status="running",
        progress_percent=0,
        current_count=0,
        total_count=0,
        start_time=datetime.now(),
        user=request.user if request.user.is_authenticated else None,
    )

    def thread_target():
        """Target function for background thread."""
        try:
            sync_function(request, job_tracker)

            if job_tracker.status == "running":
                job_tracker.status = "completed"
                job_tracker.save()

        except Exception as error:
            job_tracker.status = "failed"
            job_tracker.error_messages = [str(error)]
            job_tracker.end_time = datetime.now()
            job_tracker.save()

    thread = threading.Thread(target=thread_target, daemon=True)
    thread.start()

    return job_tracker
