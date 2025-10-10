from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.job_level_form import JobLevelForm
from core.models.job_level import JobLevel
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def job_level_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        job_level = JobLevel.objects.get(id=model_id)
    except JobLevel.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = JobLevelForm(request.POST, instance=job_level)
        if form.is_valid():
            form.save()
            return redirect('job_level')
    else:
        form = JobLevelForm(instance=job_level)

    return base_render(
        request=request,
        template_name='authenticated/job_level/job_level_form.html',
        context={'form': form}
    )
