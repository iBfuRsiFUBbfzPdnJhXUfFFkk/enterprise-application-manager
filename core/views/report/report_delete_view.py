from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.report import Report
from core.views.generic.generic_500 import generic_500


def report_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        report = Report.objects.get(id=model_id)
        report.delete()
    except Report.DoesNotExist:
        return generic_500(request=request)

    return redirect('report')
