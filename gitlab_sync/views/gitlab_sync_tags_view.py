from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncTag


def gitlab_sync_tags_view(request: HttpRequest) -> HttpResponse:
    """
    GitLab Tags list view with search and filtering.
    """
    search_query = request.GET.get("search", "").strip()

    tags = GitLabSyncTag.objects.all().select_related("project", "repository").order_by("-commit_created_at", "name")

    if search_query:
        tags = tags.filter(name__icontains=search_query) | tags.filter(
            project__path_with_namespace__icontains=search_query
        ) | tags.filter(commit_title__icontains=search_query)

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/tags.html",
        context={
            "tags": tags,
            "total_count": tags.count(),
            "search_query": search_query,
        },
    )
