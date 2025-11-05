from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncTag


def gitlab_sync_tag_detail_view(request: HttpRequest, tag_id: int) -> HttpResponse:
    """
    GitLab Tag detail view showing comprehensive information.
    """
    tag = get_object_or_404(
        GitLabSyncTag.objects.select_related("project", "repository"),
        id=tag_id,
    )

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/tag_detail.html",
        context={
            "tag": tag,
        },
    )
