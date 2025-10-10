from django.http import HttpRequest, HttpResponse

from core.models.job_level import JobLevel
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def job_level_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        job_level = JobLevel.objects.get(id=model_id)
        historical_records = job_level.history.all()
    except JobLevel.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/job_level/job_level_detail.html',
        context={
            'job_level': job_level,
            'historical_records': historical_records,
        }
    )
