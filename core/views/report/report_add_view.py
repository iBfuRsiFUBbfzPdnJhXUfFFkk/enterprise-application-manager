from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.report_form import ReportForm
from core.utilities.base_render import base_render


def report_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('report')
    else:
        form = ReportForm()

    return base_render(
        request=request,
        template_name='authenticated/report/report_form.html',
        context={'form': form}
    )
