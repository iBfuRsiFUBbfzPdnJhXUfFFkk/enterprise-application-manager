from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncEpic


def gitlab_sync_epic_detail_view(request: HttpRequest, epic_id: int) -> HttpResponse:
    """
    GitLab Epic detail view showing comprehensive information.
    """
    epic = get_object_or_404(
        GitLabSyncEpic.objects.select_related("group", "author", "parent_epic").prefetch_related(
            "issues", "child_epics"
        ),
        id=epic_id,
    )

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/epic_detail.html",
        context={
            "epic": epic,
            "issues_count": epic.issues.count(),
            "child_epics_count": epic.child_epics.count(),
        },
    )
