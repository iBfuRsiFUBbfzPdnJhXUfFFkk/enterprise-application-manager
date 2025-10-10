from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.cron_job_form import CronJobForm
from core.models.cron_job import CronJob
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def cron_job_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """
    Edit an existing cron job.
    """
    try:
        model = CronJob.objects.get(id=model_id)
    except CronJob.DoesNotExist:
        return generic_500(request, exception=Exception(f'CronJob with id {model_id} does not exist'))

    if request.method == 'POST':
        form = CronJobForm(request.POST, instance=model)
        if form.is_valid():
            form.save()
            return redirect(to='cron_job')
    else:
        form = CronJobForm(instance=model)

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/cron_job/cron_job_form.html'
    )
