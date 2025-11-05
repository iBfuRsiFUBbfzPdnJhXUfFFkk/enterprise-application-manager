from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncGroup


def gitlab_sync_group_detail_view(request: HttpRequest, group_id: int) -> HttpResponse:
    """
    GitLab Group detail view showing comprehensive information.
    """
    group = get_object_or_404(
        GitLabSyncGroup.objects.prefetch_related(
            "projects", "epics", "issues", "merge_requests"
        ),
        id=group_id,
    )

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/group_detail.html",
        context={
            "group": group,
            "projects_count": group.projects.count(),
            "epics_count": group.epics.count(),
            "issues_count": group.issues.count(),
            "merge_requests_count": group.merge_requests.count(),
        },
    )
