from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncSnippet


def gitlab_sync_snippets_view(request: HttpRequest) -> HttpResponse:
    """
    GitLab Snippets list view with search and filtering.
    """
    search_query = request.GET.get("search", "").strip()

    snippets = GitLabSyncSnippet.objects.all().select_related("project", "author").order_by("-updated_at")

    if search_query:
        snippets = snippets.filter(title__icontains=search_query) | snippets.filter(
            description__icontains=search_query
        ) | snippets.filter(file_name__icontains=search_query)

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/snippets.html",
        context={
            "snippets": snippets,
            "total_count": snippets.count(),
            "search_query": search_query,
        },
    )
