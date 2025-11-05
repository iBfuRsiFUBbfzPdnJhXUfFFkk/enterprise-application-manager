from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncPipeline


def gitlab_sync_pipelines_view(request: HttpRequest) -> HttpResponse:
    """
    GitLab Pipelines list view with search and filtering.
    """
    search_query = request.GET.get("search", "").strip()
    status_filter = request.GET.get("status", "").strip()

    pipelines = GitLabSyncPipeline.objects.all().select_related("project", "user").order_by("-created_at")

    if search_query:
        pipelines = pipelines.filter(ref__icontains=search_query) | pipelines.filter(
            sha__icontains=search_query
        )

    if status_filter:
        pipelines = pipelines.filter(status=status_filter)

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/pipelines.html",
        context={
            "pipelines": pipelines,
            "total_count": pipelines.count(),
            "search_query": search_query,
            "status_filter": status_filter,
        },
    )
