from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncCommit


def gitlab_sync_commit_detail_view(request: HttpRequest, sha: str) -> HttpResponse:
    """
    GitLab Commit detail view showing comprehensive information.
    """
    commit = get_object_or_404(
        GitLabSyncCommit.objects.select_related("project", "repository", "author"),
        sha=sha,
    )

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/commit_detail.html",
        context={
            "commit": commit,
            "pipelines_count": commit.pipelines.count(),
        },
    )
