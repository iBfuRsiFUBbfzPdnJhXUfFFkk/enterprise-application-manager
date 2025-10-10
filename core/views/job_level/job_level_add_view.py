from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.job_level_form import JobLevelForm
from core.utilities.base_render import base_render


def job_level_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = JobLevelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_level')
    else:
        form = JobLevelForm()

    return base_render(
        request=request,
        template_name='authenticated/job_level/job_level_form.html',
        context={'form': form}
    )
