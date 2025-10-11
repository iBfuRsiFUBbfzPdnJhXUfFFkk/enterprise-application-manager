from django.http import HttpRequest, HttpResponse

from core.models.job_title import JobTitle
from core.views.generic.generic_view import generic_view


def job_title_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        additional_context={'job_titles': JobTitle.objects.all()},
        model_cls=JobTitle,
        name='job_title',
        request=request,
    )
