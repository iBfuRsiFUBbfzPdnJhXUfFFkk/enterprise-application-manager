from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncMergeRequest


def gitlab_sync_merge_request_detail_view(request: HttpRequest, merge_request_id: int) -> HttpResponse:
    """
    GitLab Merge Request detail view showing comprehensive information.
    """
    merge_request = get_object_or_404(
        GitLabSyncMergeRequest.objects.select_related(
            "project", "author", "head_pipeline", "merged_by", "closed_by"
        ).prefetch_related("assignees", "reviewers", "pipelines"),
        id=merge_request_id,
    )

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/merge_request_detail.html",
        context={
            "merge_request": merge_request,
            "assignees": merge_request.assignees.all(),
            "reviewers": merge_request.reviewers.all(),
            "pipelines_count": merge_request.pipelines.count(),
        },
    )
