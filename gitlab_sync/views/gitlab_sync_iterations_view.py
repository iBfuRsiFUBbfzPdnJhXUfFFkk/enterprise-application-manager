from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncIteration


def gitlab_sync_iterations_view(request: HttpRequest) -> HttpResponse:
    """
    GitLab Iterations list view with search and filtering.
    """
    search_query = request.GET.get("search", "").strip()

    iterations = GitLabSyncIteration.objects.all().select_related("group").order_by("-start_date", "-sequence")

    if search_query:
        iterations = iterations.filter(title__icontains=search_query) | iterations.filter(
            description__icontains=search_query
        ) | iterations.filter(group__path__icontains=search_query)

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/iterations.html",
        context={
            "iterations": iterations,
            "total_count": iterations.count(),
            "search_query": search_query,
        },
    )
