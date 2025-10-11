from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.report_form import ReportForm
from core.models.report import Report
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def report_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        report = Report.objects.get(id=model_id)
    except Report.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('report')
    else:
        form = ReportForm(instance=report)

    return base_render(
        request=request,
        template_name='authenticated/report/report_form.html',
        context={'form': form}
    )
