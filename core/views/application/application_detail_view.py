from typing import Mapping, Any
from django.http import HttpRequest, HttpResponse

from core.models.application import Application
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def application_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        application = Application.objects.get(id=model_id)
    except Application.DoesNotExist:
        return generic_500(request=request)

    # Get created and updated history records
    created_record = application.history.order_by('history_date').first()
    updated_record = application.history.order_by('-history_date').first()

    context: Mapping[str, Any] = {
        'model': application,
        'created_record': created_record,
        'updated_record': updated_record,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/application/application_detail.html'
    )
