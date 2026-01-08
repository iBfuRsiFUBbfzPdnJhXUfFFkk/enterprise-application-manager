from django.http import HttpRequest, HttpResponse

from core.models.maintenance_window import MaintenanceWindow
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def maintenance_window_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        maintenance_window = MaintenanceWindow.objects.get(id=model_id)
        historical_records = maintenance_window.history.all()
    except MaintenanceWindow.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/maintenance_window/maintenance_window_detail.html',
        context={
            'maintenance_window': maintenance_window,
            'historical_records': historical_records,
        }
    )
