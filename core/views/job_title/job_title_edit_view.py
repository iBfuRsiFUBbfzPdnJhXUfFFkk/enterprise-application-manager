from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.job_title_form import JobTitleForm
from core.models.job_title import JobTitle
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def job_title_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        job_title = JobTitle.objects.get(id=model_id)
    except JobTitle.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = JobTitleForm(request.POST, instance=job_title)
        if form.is_valid():
            form.save()
            return redirect('job_title')
    else:
        form = JobTitleForm(instance=job_title)

    return base_render(
        request=request,
        template_name='authenticated/job_title/job_title_form.html',
        context={'form': form}
    )
