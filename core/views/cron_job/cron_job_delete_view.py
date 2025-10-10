from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.cron_job import CronJob
from core.views.generic.generic_500 import generic_500


def cron_job_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """
    Delete a cron job.
    """
    try:
        cron_job = CronJob.objects.get(id=model_id)
        cron_job.delete()
    except CronJob.DoesNotExist:
        return generic_500(request=request)

    return redirect(to='cron_job')
