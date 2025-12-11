import json
from typing import Any, Mapping
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from core.models.api_request import APIRequest
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


@ensure_csrf_cookie
def api_request_detail_view(
    request: HttpRequest, model_id: int
) -> HttpResponse:
    try:
        api_request = APIRequest.objects.get(id=model_id)
    except APIRequest.DoesNotExist:
        return generic_500(request=request)

    created_record = api_request.history.order_by('history_date').first()
    updated_record = api_request.history.order_by('-history_date').first()

    # Get recent executions for this request
    recent_executions = api_request.executions.all()[:10]

    # Get environment URLs
    environment_urls = {}
    if api_request.api:
        environment_urls = {
            'Local': api_request.api.url_local or '',
            'Development': api_request.api.url_development or '',
            'Staging': api_request.api.url_staging or '',
            'Production': api_request.api.url_production or '',
            'Production External': api_request.api.url_production_external or '',
        }

    context: Mapping[str, Any] = {
        'model': api_request,
        'api_request': api_request,
        'created_record': created_record,
        'updated_record': updated_record,
        'recent_executions': recent_executions,
        'environment_urls_json': json.dumps(environment_urls),
    }
    return base_render(
        context=context,
        request=request,
        template_name='authenticated/api_request/api_request_detail.html',
    )
