import threading
from typing import Callable

from django.http import HttpRequest
from django.utils import timezone

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
    from django.db import connection

    job_tracker = GitLabSyncJobTracker.objects.create(
        job_type=job_type,
        status="running",
        progress_percent=0,
        current_count=0,
        total_count=0,
        start_time=timezone.now(),
        user=request.user if request.user.is_authenticated else None,
    )

    print(f"[RunSync] Created job tracker {job_tracker.id} for {job_type}")

    def thread_target():
        """Target function for background thread."""
        try:
            # Close the old database connection to force a new one in this thread
            connection.close()

            print(f"[RunSync] Starting sync function for job {job_tracker.id}")
            sync_function(request, job_tracker)

            # Refresh from database and check status
            job_tracker.refresh_from_db()
            if job_tracker.status == "running":
                job_tracker.status = "completed"
                job_tracker.save()
                print(f"[RunSync] Job {job_tracker.id} completed successfully")

        except Exception as error:
            print(f"[RunSync] Job {job_tracker.id} failed with error: {error}")
            import traceback

            error_trace = traceback.format_exc()
            traceback.print_exc()

            try:
                job_tracker.refresh_from_db()
                job_tracker.status = "failed"

                # Add detailed error information to logs
                error_timestamp = timezone.now().strftime("%H:%M:%S")
                if not job_tracker.detailed_logs:
                    job_tracker.detailed_logs = []
                job_tracker.detailed_logs.append(
                    f"[{error_timestamp}] ❌ Critical error: {str(error)}"
                )
                job_tracker.detailed_logs.append(
                    f"[{error_timestamp}] Stack trace: {error_trace}"
                )

                if not job_tracker.error_messages:
                    job_tracker.error_messages = []
                job_tracker.error_messages.append(str(error))
                job_tracker.end_time = timezone.now()
                job_tracker.save()
                print(f"[RunSync] Job {job_tracker.id} marked as failed")
            except Exception as update_error:
                print(f"[RunSync] CRITICAL: Failed to update job tracker on error: {update_error}")
                traceback.print_exc()

        finally:
            # Final safety net - ensure job is never left in "running" state
            try:
                job_tracker.refresh_from_db()
                if job_tracker.status == "running":
                    print(f"[RunSync] WARNING: Job {job_tracker.id} still running after completion, forcing failure state")
                    job_tracker.status = "failed"
                    error_timestamp = timezone.now().strftime("%H:%M:%S")
                    if not job_tracker.detailed_logs:
                        job_tracker.detailed_logs = []
                    job_tracker.detailed_logs.append(
                        f"[{error_timestamp}] ⚠️ Job did not complete normally - forced to failed state"
                    )
                    if not job_tracker.error_messages:
                        job_tracker.error_messages = []
                    job_tracker.error_messages.append("Job did not update status properly - possible permission or database error")
                    job_tracker.end_time = timezone.now()
                    job_tracker.save()
            except Exception as final_error:
                print(f"[RunSync] CRITICAL: Failed final safety update for job {job_tracker.id}: {final_error}")
                traceback.print_exc()

    thread = threading.Thread(target=thread_target, daemon=True)
    thread.start()

    return job_tracker
