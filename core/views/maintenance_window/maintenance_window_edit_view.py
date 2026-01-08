from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.maintenance_window_form import MaintenanceWindowForm
from core.models.maintenance_window import MaintenanceWindow
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def maintenance_window_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        maintenance_window = MaintenanceWindow.objects.get(id=model_id)
    except MaintenanceWindow.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = MaintenanceWindowForm(request.POST, instance=maintenance_window)
        if form.is_valid():
            form.save()
            return redirect('maintenance_window')
    else:
        form = MaintenanceWindowForm(instance=maintenance_window)

    return base_render(
        request=request,
        template_name='authenticated/maintenance_window/maintenance_window_form.html',
        context={'form': form}
    )
