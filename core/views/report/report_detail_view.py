from django.http import HttpRequest, HttpResponse

from core.models.report import Report
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def report_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        report = Report.objects.get(id=model_id)
        historical_records = report.history.all()
    except Report.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/report/report_detail.html',
        context={
            'report': report,
            'historical_records': historical_records,
        }
    )
