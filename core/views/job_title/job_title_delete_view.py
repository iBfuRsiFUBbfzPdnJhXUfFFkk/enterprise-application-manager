from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.job_title import JobTitle
from core.views.generic.generic_500 import generic_500


def job_title_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        job_title = JobTitle.objects.get(id=model_id)
        job_title.delete()
    except JobTitle.DoesNotExist:
        return generic_500(request=request)

    return redirect('job_title')
