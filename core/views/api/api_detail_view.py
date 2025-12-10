from typing import Any, Mapping
from django.http import HttpRequest, HttpResponse
from core.models.api import API
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def api_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        api = API.objects.get(id=model_id)
    except API.DoesNotExist:
        return generic_500(request=request)

    created_record = api.history.order_by('history_date').first()
    updated_record = api.history.order_by('-history_date').first()

    # Get authentications and requests for this API
    authentications = api.authentications.all()
    api_requests = api.requests.all()

    context: Mapping[str, Any] = {
        'model': api,
        'created_record': created_record,
        'updated_record': updated_record,
        'authentications': authentications,
        'api_requests': api_requests,
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/api/api_detail.html',
    )
