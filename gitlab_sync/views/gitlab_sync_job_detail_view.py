from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncJob


def gitlab_sync_job_detail_view(request: HttpRequest, job_id: int) -> HttpResponse:
    """
    GitLab Job detail view showing comprehensive information.
    """
    job = get_object_or_404(
        GitLabSyncJob.objects.select_related("pipeline", "project", "user").prefetch_related("artifacts"),
        id=job_id,
    )

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/job_detail.html",
        context={
            "job": job,
            "artifacts_count": job.artifacts.count(),
        },
    )
