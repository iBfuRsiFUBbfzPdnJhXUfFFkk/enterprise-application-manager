from datetime import datetime, UTC
from time import time
from typing import TypedDict

from django.http import HttpRequest, HttpResponse
from requests import get, Response

from core.models.person import Person
from core.models.secret import Secret
from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


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


def this_api_sync_gitlab_users_view(request: HttpRequest) -> HttpResponse:
    start_time: float = time()
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
    gitlab_user_objects: list[GitlabApiResponseMember] = []
    while url is not None:
        response: Response = get(headers=headers, url=url)
        response.raise_for_status()
        gitlab_user_objects.extend(response.json())
        url: str | None = response.links.get("next", {}).get("url")
    for gitlab_user_object in gitlab_user_objects:
        gitlab_access_level_int: int | None = gitlab_user_object.get("access_level", None)
        gitlab_id_int: int | None = gitlab_user_object.get("id", None)
        gitlab_name: str | None = gitlab_user_object.get("name", None)
        gitlab_names: list[str] = (gitlab_name or "").split(" ")
        gitlab_username: str | None = gitlab_user_object.get("username", None)
        gitlab_first_name: str = gitlab_names[0] if len(gitlab_names) > 0 else ""
        gitlab_last_name: str = gitlab_names[1] if len(gitlab_names) > 1 else ""
        person: Person | None = Person.objects.filter(
            gitlab_sync_id=str(object=gitlab_id_int),
            gitlab_sync_id__isnull=False,
        ).first()
        if person is None:
            person: Person | None = Person.objects.filter(
                gitlab_sync_username=gitlab_username,
                gitlab_sync_username__isnull=False,
            ).first()
            if person is None:
                person: Person | None = Person.objects.filter(
                    name_first=gitlab_first_name,
                    name_first__isnull=False,
                    name_last=gitlab_last_name,
                    name_last__isnull=False,
                ).first()
                if person is None:
                    person: Person = Person.objects.create(
                        name_first=gitlab_first_name,
                        name_last=gitlab_last_name,
                    )
        person.gitlab_sync_access_level = str(
            object=gitlab_access_level_int) if gitlab_access_level_int is not None else None
        person.gitlab_sync_avatar_url = gitlab_user_object.get("avatar_url", None)
        person.gitlab_sync_datetime_created_at = parse_datetime(datetime_str=gitlab_user_object.get("created_at", None))
        person.gitlab_sync_datetime_expires_at = parse_datetime(datetime_str=gitlab_user_object.get("expires_at", None))
        person.gitlab_sync_id = str(object=gitlab_id_int) if gitlab_id_int is not None else None
        person.gitlab_sync_is_locked = gitlab_user_object.get("locked", False)
        person.gitlab_sync_membership_state = gitlab_user_object.get("membership_state", None)
        person.gitlab_sync_name = gitlab_name
        person.gitlab_sync_state = gitlab_user_object.get("state", None)
        person.gitlab_sync_username = gitlab_username
        person.gitlab_sync_web_url = gitlab_user_object.get("web_url", None)
        person.save()
    end_time: float = time()
    execution_time_in_seconds: float = end_time - start_time
    print(f'Execution time: {execution_time_in_seconds} seconds')
    return base_render(
        context={"execution_time_in_seconds": execution_time_in_seconds},
        request=request,
        template_name="authenticated/action/action_success.html"
    )
