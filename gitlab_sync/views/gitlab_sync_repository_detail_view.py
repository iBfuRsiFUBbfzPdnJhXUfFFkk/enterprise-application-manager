from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncRepository


def gitlab_sync_repository_detail_view(request: HttpRequest, repository_id: int) -> HttpResponse:
    """
    GitLab Repository detail view showing comprehensive information.
    """
    repository = get_object_or_404(
        GitLabSyncRepository.objects.select_related("project"),
        id=repository_id,
    )

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/repository_detail.html",
        context={
            "repository": repository,
            "branches_count": repository.branches.count(),
            "tags_count": repository.tags.count(),
            "commits_count": repository.commits.count(),
        },
    )
