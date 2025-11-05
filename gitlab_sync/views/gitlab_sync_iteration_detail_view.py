from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncIteration


def gitlab_sync_iteration_detail_view(
    request: HttpRequest, iteration_id: int
) -> HttpResponse:
    """
    GitLab Iteration detail view showing comprehensive information.
    """
    iteration = get_object_or_404(
        GitLabSyncIteration.objects.select_related("group"),
        id=iteration_id,
    )

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/iteration_detail.html",
        context={
            "iteration": iteration,
            "issues_count": iteration.issues.count(),
            "merge_requests_count": iteration.merge_requests.count(),
        },
    )
