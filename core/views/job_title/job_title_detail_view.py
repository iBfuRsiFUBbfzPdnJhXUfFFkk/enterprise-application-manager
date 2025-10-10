from django.http import HttpRequest, HttpResponse

from core.models.job_title import JobTitle
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def job_title_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        job_title = JobTitle.objects.get(id=model_id)
        historical_records = job_title.history.all()
    except JobTitle.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/job_title/job_title_detail.html',
        context={
            'job_title': job_title,
            'historical_records': historical_records,
        }
    )
