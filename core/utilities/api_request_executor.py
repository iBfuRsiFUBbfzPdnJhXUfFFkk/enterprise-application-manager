import base64
from typing import Any
import requests
from core.models.api import API
from core.models.api_request import APIRequest
from core.models.api_authentication import APIAuthentication


def get_base_url_for_environment(api: API, environment: str) -> str:
    """Get the base URL for the specified environment."""
    url_map = {
        'Local': api.url_local,
        'Development': api.url_development,
        'Staging': api.url_staging,
        'Production': api.url_production,
        'Production External': api.url_production_external,
    }
    return url_map.get(environment, '') or ''


def replace_path_parameters(url_path: str, params: dict[str, str]) -> str:
    """Replace {param} placeholders with actual values."""
    if not params:
        return url_path

    result = url_path
    for key, value in params.items():
        result = result.replace(f'{{{key}}}', str(value))
    return result


def prepare_headers(
    api_request: APIRequest, custom_headers: dict[str, str]
) -> dict[str, str]:
    """Prepare headers including authentication."""
    headers = {}

    if api_request.authentication:
        auth = api_request.authentication

        if auth.auth_type == 'API Key':
            if auth.api_key_location == 'Header' and auth.secret_api_key:
                key_value = auth.secret_api_key.get_encrypted_value()
                if key_value and auth.api_key_name:
                    headers[auth.api_key_name] = key_value

        elif auth.auth_type == 'Bearer Token' and auth.secret_bearer_token:
            token = auth.secret_bearer_token.get_encrypted_value()
            if token:
                headers['Authorization'] = f'Bearer {token}'

        elif auth.auth_type == 'Basic Auth':
            if auth.basic_auth_username and auth.secret_basic_auth_password:
                username = auth.basic_auth_username
                password = auth.secret_basic_auth_password.get_encrypted_value()
                if password:
                    credentials = base64.b64encode(
                        f'{username}:{password}'.encode()
                    ).decode()
                    headers['Authorization'] = f'Basic {credentials}'

    # Add custom headers (override auth headers if needed)
    if custom_headers:
        headers.update(custom_headers)

    return headers


def execute_http_request(
    method: str,
    url: str,
    headers: dict[str, str],
    params: dict[str, Any],
    data: str | None,
) -> requests.Response:
    """Execute the HTTP request."""
    return requests.request(
        method=method, url=url, headers=headers, params=params, data=data, timeout=30
    )
