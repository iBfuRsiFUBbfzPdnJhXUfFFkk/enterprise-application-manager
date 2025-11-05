from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncRepository


def gitlab_sync_repositories_view(request: HttpRequest) -> HttpResponse:
    """
    GitLab Repositories list view with search and filtering.
    """
    search_query = request.GET.get("search", "").strip()

    repositories = GitLabSyncRepository.objects.all().select_related("project").order_by("-id")

    if search_query:
        repositories = repositories.filter(name__icontains=search_query) | repositories.filter(
            project__path_with_namespace__icontains=search_query
        ) | repositories.filter(default_branch__icontains=search_query)

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/repositories.html",
        context={
            "repositories": repositories,
            "total_count": repositories.count(),
            "search_query": search_query,
        },
    )
