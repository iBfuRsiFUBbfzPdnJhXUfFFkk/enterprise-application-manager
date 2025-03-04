from datetime import datetime, UTC
from time import time

from django.http import HttpRequest, HttpResponse
from gitlab import Gitlab
from gitlab.base import RESTObjectList

from core.models.person import Person
from core.utilities.base_render import base_render
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.utilities.git_lab.get_git_lab_group_id import get_git_lab_group_id
from core.views.generic.generic_500 import generic_500


def parse_datetime(datetime_str: str | None) -> datetime | None:
    if datetime_str is None:
        return None
    dt: datetime = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.replace(tzinfo=UTC)


def this_api_sync_gitlab_users_view(request: HttpRequest) -> HttpResponse:
    start_time: float = time()
    git_lab_client: Gitlab | None = get_git_lab_client()
    git_lab_group_id: str | None = get_git_lab_group_id()
    if git_lab_client is None or git_lab_group_id is None:
        return generic_500(request=request)
    group_members: RESTObjectList = git_lab_client.groups.get(id=git_lab_group_id).members.list(all=True)
    for group_member in group_members:
        gitlab_access_level_int: int | None = group_member.access_level
        gitlab_id_int: int | None = group_member.id
        gitlab_name: str | None = group_member.name
        gitlab_names: list[str] = (gitlab_name or "").split(" ")
        gitlab_username: str | None = group_member.username
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
        person.gitlab_sync_avatar_url = group_member.avatar_url
        person.gitlab_sync_datetime_created_at = parse_datetime(datetime_str=group_member.created_at)
        person.gitlab_sync_datetime_expires_at = parse_datetime(datetime_str=group_member.expires_at)
        person.gitlab_sync_id = str(object=gitlab_id_int) if gitlab_id_int is not None else None
        person.gitlab_sync_is_locked = group_member.locked
        person.gitlab_sync_membership_state = group_member.membership_state
        person.gitlab_sync_name = gitlab_name
        person.gitlab_sync_state = group_member.state
        person.gitlab_sync_username = gitlab_username
        person.gitlab_sync_web_url = group_member.web_url
        person.save()
    end_time: float = time()
    execution_time_in_seconds: float = end_time - start_time
    return base_render(
        context={"execution_time_in_seconds": execution_time_in_seconds},
        request=request,
        template_name="authenticated/action/action_success.html"
    )
