from datetime import datetime, UTC
from time import time
from typing import TypedDict

from django.http import HttpRequest, HttpResponse

from core.models.secret import Secret
from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500
from core.views.this_api.this_api_update_code_churn_view.fetch_merged_pull_requests import fetch_merged_pull_requests


class GitlabApiResponseMember(TypedDict):
    access_level: int | None
    avatar_url: str | None
    created_at: str | None
    expires_at: str | None
    id: int | None
    locked: bool | None
    membership_state: str | None
    name: str | None
    state: str | None
    username: str | None
    web_url: str | None


def parse_datetime(datetime_str: str | None) -> datetime | None:
    if datetime_str is None:
        return None
    dt: datetime = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.replace(tzinfo=UTC)


def this_api_update_code_churn_view(request: HttpRequest) -> HttpResponse:
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
    fetch_merged_pull_requests(
        connection_gitlab_hostname=connection_gitlab_hostname,
        connection_gitlab_api_version=connection_gitlab_api_version,
        connection_gitlab_group_id=connection_gitlab_group_id,
        decrypted_token=decrypted_token,
        merged_after="2025-01-01T00:00:00Z",
        merged_before="2025-02-01T00:00:00Z",
    )

    end_time: float = time()
    execution_time_in_seconds: float = end_time - start_time
    return base_render(
        context={"execution_time_in_seconds": execution_time_in_seconds},
        request=request,
        template_name="authenticated/action/action_success.html"
    )
