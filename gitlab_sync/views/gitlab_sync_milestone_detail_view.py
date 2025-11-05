from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncMilestone


def gitlab_sync_milestone_detail_view(
    request: HttpRequest, milestone_id: int
) -> HttpResponse:
    """
    GitLab Milestone detail view showing comprehensive information.
    """
    milestone = get_object_or_404(
        GitLabSyncMilestone.objects.select_related("project", "group"),
        id=milestone_id,
    )

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/milestone_detail.html",
        context={
            "milestone": milestone,
            "issues_count": milestone.issues.count(),
            "merge_requests_count": milestone.merge_requests.count(),
        },
    )
