from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.job_title_form import JobTitleForm
from core.utilities.base_render import base_render


def job_title_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = JobTitleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_title')
    else:
        form = JobTitleForm()

    return base_render(
        request=request,
        template_name='authenticated/job_title/job_title_form.html',
        context={'form': form}
    )
