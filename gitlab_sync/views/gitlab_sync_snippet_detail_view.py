from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncSnippet


def gitlab_sync_snippet_detail_view(
    request: HttpRequest, snippet_id: int
) -> HttpResponse:
    """
    GitLab Snippet detail view showing comprehensive information.
    """
    snippet = get_object_or_404(
        GitLabSyncSnippet.objects.select_related("project", "author"),
        id=snippet_id,
    )

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/snippet_detail.html",
        context={
            "snippet": snippet,
        },
    )
