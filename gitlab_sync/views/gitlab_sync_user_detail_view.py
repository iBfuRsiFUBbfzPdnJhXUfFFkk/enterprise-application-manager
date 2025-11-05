from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncUser


def gitlab_sync_user_detail_view(request: HttpRequest, user_id: int) -> HttpResponse:
    """
    GitLab User detail view showing comprehensive information.
    """
    user = get_object_or_404(
        GitLabSyncUser.objects.select_related("person").prefetch_related(
            "commits_authored", "issues_authored", "merge_requests_authored", "jobs_triggered"
        ),
        id=user_id,
    )

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/user_detail.html",
        context={
            "user": user,
            "commits_count": user.commits_authored.count(),
            "issues_count": user.issues_authored.count(),
            "merge_requests_count": user.merge_requests_authored.count(),
            "jobs_count": user.jobs_triggered.count(),
        },
    )
