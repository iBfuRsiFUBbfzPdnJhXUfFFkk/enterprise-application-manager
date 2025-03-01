from time import time

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from requests import get

from core.models.secret import Secret
from core.models.this_server_configuration import ThisServerConfiguration
from core.views.generic.generic_500 import generic_500


def this_api_sync_gitlab_users_view(request: HttpRequest) -> HttpResponse:
    start_time: float = time()
    print('Syncing GitLab users...')
    this_server_configuration: ThisServerConfiguration | None = ThisServerConfiguration.objects.last()
    if this_server_configuration is None:
        return generic_500(request=request)
    connection_gitlab_hostname: str | None = this_server_configuration.connection_gitlab_hostname
    if connection_gitlab_hostname is None:
        return generic_500(request=request)
    connection_gitlab_api_version: str | None = this_server_configuration.connection_gitlab_api_version
    if connection_gitlab_api_version is None:
        return generic_500(request=request)
    connection_gitlab_group_id: str | None = this_server_configuration.connection_gitlab_group_id
    if connection_gitlab_group_id is None:
        return generic_500(request=request)
    connection_gitlab_token_secret: Secret | None = this_server_configuration.connection_gitlab_token
    if connection_gitlab_token_secret is None:
        return generic_500(request=request)
    decrypted_token: str | None = connection_gitlab_token_secret.get_encrypted_value()
    if decrypted_token is None:
        return generic_500(request=request)
    headers: dict[str, str] = {"PRIVATE-TOKEN": decrypted_token}
    url: str = f"https://{connection_gitlab_hostname}/api/{connection_gitlab_api_version}/groups/{connection_gitlab_group_id}/members"
    response = get(headers=headers, url=url)
    response.raise_for_status()
    print(response.json())
    end_time: float = time()
    execution_time: float = end_time - start_time
    print(f'Execution time: {execution_time} seconds')
    return render(context={}, request=request, template_name="home.html")
