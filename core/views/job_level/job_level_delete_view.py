from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.job_level import JobLevel
from core.views.generic.generic_500 import generic_500


def job_level_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        job_level = JobLevel.objects.get(id=model_id)
        job_level.delete()
    except JobLevel.DoesNotExist:
        return generic_500(request=request)

    return redirect('job_level')
