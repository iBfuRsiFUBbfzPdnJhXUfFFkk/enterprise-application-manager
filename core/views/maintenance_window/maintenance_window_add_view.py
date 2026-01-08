from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.maintenance_window_form import MaintenanceWindowForm
from core.utilities.base_render import base_render


def maintenance_window_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = MaintenanceWindowForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maintenance_window')
    else:
        form = MaintenanceWindowForm()

    return base_render(
        request=request,
        template_name='authenticated/maintenance_window/maintenance_window_form.html',
        context={'form': form}
    )
