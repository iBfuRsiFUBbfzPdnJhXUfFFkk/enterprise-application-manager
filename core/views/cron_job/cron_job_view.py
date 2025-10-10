from django.http import HttpRequest, HttpResponse

from core.models.cron_job import CronJob
from core.views.generic.generic_view import generic_view


def cron_job_view(request: HttpRequest) -> HttpResponse:
    """
    List all cron jobs.
    """
    return generic_view(
        model_cls=CronJob,
        name='cron_job',
        request=request,
    )
