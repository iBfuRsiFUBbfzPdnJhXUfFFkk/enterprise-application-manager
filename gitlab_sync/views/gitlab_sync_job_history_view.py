from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncJobTracker


def gitlab_sync_job_history_view(request: HttpRequest) -> HttpResponse:
    """
    Job history page showing all past sync operations.

    Displays job status, duration, counts, and allows viewing detailed logs.
    """
    # Filter by status if provided
    status_filter = request.GET.get("status", "all")

    if status_filter == "all":
        jobs = GitLabSyncJobTracker.objects.all()
    else:
        jobs = GitLabSyncJobTracker.objects.filter(status=status_filter)

    jobs = jobs.order_by("-start_time")[:100]  # Last 100 jobs

    context = {
        "jobs": jobs,
        "status_filter": status_filter,
    }

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/job_history.html",
        context=context,
    )
