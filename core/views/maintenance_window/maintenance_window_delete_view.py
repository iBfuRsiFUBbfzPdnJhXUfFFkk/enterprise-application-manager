from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.maintenance_window import MaintenanceWindow
from core.views.generic.generic_500 import generic_500


def maintenance_window_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        maintenance_window = MaintenanceWindow.objects.get(id=model_id)
        maintenance_window.delete()
    except MaintenanceWindow.DoesNotExist:
        return generic_500(request=request)

    return redirect('maintenance_window')
