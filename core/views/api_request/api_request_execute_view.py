import json
import time
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_POST
from core.models.api_request import APIRequest
from core.models.api_request_execution import APIRequestExecution
from core.utilities.api_request_executor import (
    execute_http_request,
    get_base_url_for_environment,
    prepare_headers,
    replace_path_parameters,
)
from core.utilities.get_user_from_request import get_user_from_request


@require_POST
def api_request_execute_view(
    request: HttpRequest, request_id: int
) -> JsonResponse:
    """Execute an API request with provided parameters."""
    try:
        api_request = APIRequest.objects.get(id=request_id)

        # Parse JSON data
        data = json.loads(request.body)
        environment = data.get('environment', api_request.default_environment)
        path_params = data.get('path_parameters', {})
        query_params = data.get('query_parameters', {})
        custom_headers = data.get('custom_headers', {})
        content_type = data.get('content_type', api_request.content_type or 'application/json')
        form_data = data.get('form_data', {})
        body = data.get('body', api_request.request_body or '')

        # Build the full URL
        base_url = get_base_url_for_environment(api_request.api, environment)
        if not base_url:
            return JsonResponse(
                {
                    'success': False,
                    'error': f'No URL configured for environment: {environment}',
                },
                status=400,
            )

        url_path = replace_path_parameters(api_request.url_path, path_params)
        full_url = f"{base_url.rstrip('/')}/{url_path.lstrip('/')}"

        # Prepare headers with Content-Type
        headers = prepare_headers(api_request, custom_headers)
        headers['Content-Type'] = content_type

        # Prepare request body based on content type
        if content_type == 'application/x-www-form-urlencoded':
            # URL-encode the form data
            from urllib.parse import urlencode
            request_body = urlencode(form_data) if form_data else ''
        else:
            request_body = body

        # Execute the request
        start_time = time.time()
        try:
            response = execute_http_request(
                method=api_request.http_method,
                url=full_url,
                headers=headers,
                params=query_params,
                data=request_body if request_body else None,
            )
            response_time_ms = int((time.time() - start_time) * 1000)

            # Get user's person
            user = get_user_from_request(request=request)
            person = user.person_mapping if user else None

            # Save execution record
            execution = APIRequestExecution.objects.create(
                api_request=api_request,
                executed_by=person,
                environment=environment,
                executed_url=full_url,
                executed_path_parameters=path_params,
                executed_query_parameters=query_params,
                executed_headers=headers,
                executed_body=request_body,
                response_status_code=response.status_code,
                response_headers=dict(response.headers),
                response_body=response.text[:100000],  # Limit to 100KB
                response_time_ms=response_time_ms,
                is_error=False,
            )

            return JsonResponse(
                {
                    'success': True,
                    'execution_id': execution.id,
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'body': response.text,
                    'response_time_ms': response_time_ms,
                }
            )

        except Exception as e:
            response_time_ms = int((time.time() - start_time) * 1000)

            # Get user's person
            user = get_user_from_request(request=request)
            person = user.person_mapping if user else None

            # Save error execution record
            execution = APIRequestExecution.objects.create(
                api_request=api_request,
                executed_by=person,
                environment=environment,
                executed_url=full_url,
                executed_path_parameters=path_params,
                executed_query_parameters=query_params,
                executed_headers=headers,
                executed_body=request_body,
                is_error=True,
                error_message=str(e),
                response_time_ms=response_time_ms,
            )

            return JsonResponse(
                {
                    'success': False,
                    'execution_id': execution.id,
                    'error': str(e),
                    'response_time_ms': response_time_ms,
                },
                status=500,
            )

    except APIRequest.DoesNotExist:
        return JsonResponse(
            {'success': False, 'error': 'Request not found'}, status=404
        )
    except json.JSONDecodeError as e:
        return JsonResponse(
            {'success': False, 'error': f'Invalid JSON: {str(e)}'}, status=400
        )
    except Exception as e:
        return JsonResponse(
            {'success': False, 'error': str(e)}, status=500
        )
