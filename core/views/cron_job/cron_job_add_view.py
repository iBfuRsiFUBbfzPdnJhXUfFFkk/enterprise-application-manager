from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.cron_job_form import CronJobForm
from core.utilities.base_render import base_render


def cron_job_add_view(request: HttpRequest) -> HttpResponse:
    """
    Create a new cron job.
    """
    if request.method == 'POST':
        form = CronJobForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='cron_job')
    else:
        form = CronJobForm()

    context: Mapping[str, Any] = {'form': form}
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/cron_job/cron_job_form.html'
    )
