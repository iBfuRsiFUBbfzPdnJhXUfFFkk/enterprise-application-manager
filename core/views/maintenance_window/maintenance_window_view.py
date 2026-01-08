from django.http import HttpRequest, HttpResponse

from core.models.maintenance_window import MaintenanceWindow
from core.views.generic.generic_view import generic_view


def maintenance_window_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=MaintenanceWindow,
        name='maintenance_window',
        request=request,
    )
