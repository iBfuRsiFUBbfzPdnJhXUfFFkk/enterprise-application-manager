from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncJob


def gitlab_sync_jobs_view(request: HttpRequest) -> HttpResponse:
    """
    GitLab Jobs list view with search and filtering.
    """
    search_query = request.GET.get("search", "").strip()
    status_filter = request.GET.get("status", "").strip()
    stage_filter = request.GET.get("stage", "").strip()

    jobs = GitLabSyncJob.objects.all().select_related("pipeline", "project", "user").order_by("-created_at")

    if search_query:
        jobs = jobs.filter(name__icontains=search_query)

    if status_filter:
        jobs = jobs.filter(status=status_filter)

    if stage_filter:
        jobs = jobs.filter(stage=stage_filter)

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/jobs.html",
        context={
            "jobs": jobs,
            "total_count": jobs.count(),
            "search_query": search_query,
            "status_filter": status_filter,
            "stage_filter": stage_filter,
        },
    )
