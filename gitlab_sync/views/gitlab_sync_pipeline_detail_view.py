from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncPipeline


def gitlab_sync_pipeline_detail_view(request: HttpRequest, pipeline_id: int) -> HttpResponse:
    """
    GitLab Pipeline detail view showing comprehensive information.
    """
    pipeline = get_object_or_404(
        GitLabSyncPipeline.objects.select_related("project", "user", "merge_request").prefetch_related("jobs"),
        id=pipeline_id,
    )

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/pipeline_detail.html",
        context={
            "pipeline": pipeline,
            "jobs_count": pipeline.jobs.count(),
        },
    )
