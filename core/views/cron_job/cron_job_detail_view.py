from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse

from core.models.cron_job import CronJob
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def cron_job_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """
    Display cron job details and change history.
    """
    try:
        cron_job = CronJob.objects.get(id=model_id)
        historical_records = cron_job.history.all()
    except CronJob.DoesNotExist:
        return generic_500(request, exception=Exception(f'CronJob with id {model_id} does not exist'))

    context: Mapping[str, Any] = {
        'cron_job': cron_job,
        'historical_records': historical_records,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/cron_job/cron_job_detail.html'
    )
