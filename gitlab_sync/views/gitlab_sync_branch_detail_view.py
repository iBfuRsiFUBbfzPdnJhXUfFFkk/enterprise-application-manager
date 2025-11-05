from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncBranch


def gitlab_sync_branch_detail_view(request: HttpRequest, branch_id: int) -> HttpResponse:
    """
    GitLab Branch detail view showing comprehensive information.
    """
    branch = get_object_or_404(
        GitLabSyncBranch.objects.select_related("project", "repository"),
        id=branch_id,
    )

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/branch_detail.html",
        context={
            "branch": branch,
        },
    )
