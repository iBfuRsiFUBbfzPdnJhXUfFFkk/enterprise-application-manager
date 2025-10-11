from django.http import HttpRequest, HttpResponse

from core.models.job_level import JobLevel
from core.views.generic.generic_view import generic_view


def job_level_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        additional_context={'job_levels': JobLevel.objects.all()},
        model_cls=JobLevel,
        name='job_level',
        request=request,
    )
