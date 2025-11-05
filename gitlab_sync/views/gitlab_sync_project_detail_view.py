from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncProject


def gitlab_sync_project_detail_view(request: HttpRequest, project_id: int) -> HttpResponse:
    """
    GitLab Project detail view showing comprehensive information.
    """
    project = get_object_or_404(
        GitLabSyncProject.objects.select_related("group", "application", "repository").prefetch_related(
            "issues", "merge_requests", "pipelines", "commits"
        ),
        id=project_id,
    )

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/project_detail.html",
        context={
            "project": project,
            "issues_count": project.issues.count(),
            "merge_requests_count": project.merge_requests.count(),
            "pipelines_count": project.pipelines.count(),
            "commits_count": project.commits.count(),
        },
    )
