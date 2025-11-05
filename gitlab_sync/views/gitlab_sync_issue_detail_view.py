from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncIssue


def gitlab_sync_issue_detail_view(request: HttpRequest, issue_id: int) -> HttpResponse:
    """
    GitLab Issue detail view showing comprehensive information.
    """
    issue = get_object_or_404(
        GitLabSyncIssue.objects.select_related("project", "author", "epic", "closed_by").prefetch_related(
            "assignees"
        ),
        id=issue_id,
    )

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/issue_detail.html",
        context={
            "issue": issue,
            "assignees": issue.assignees.all(),
        },
    )
