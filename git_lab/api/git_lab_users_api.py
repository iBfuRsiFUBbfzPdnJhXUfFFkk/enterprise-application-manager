from typing import cast, TypedDict

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab
from gitlab.v4.objects import GroupMember, Group

from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import convert_and_enforce_utc_timezone
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.models.git_lab_group import GitLabGroup
from git_lab.models.git_lab_user import GitLabUser


class GitLabUserBaseTypedDict(TypedDict):
    avatar_url: str | None
    id: int | None
    locked: bool | None
    name: str | None
    username: str | None
    web_url: str | None


class GitLabCreatedByTypedDict(GitLabUserBaseTypedDict):
    state: str | None


class GitLabUserTypedDict(GitLabUserBaseTypedDict):
    created_at: str | None
    created_by: GitLabCreatedByTypedDict | None
    expires_at: str | None
    membership_state: str | None


def git_lab_users_api(
        request: HttpRequest,
) -> JsonResponse | HttpResponse:
    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        return generic_500(request=request)
    git_lab_groups: QuerySet[GitLabGroup] = cast_query_set(
        typ=GitLabGroup,
        val=GitLabGroup.objects.all(),
    )
    all_members: set[GroupMember] = set()
    for git_lab_group in git_lab_groups:
        group: Group | None = git_lab_client.groups.get(id=git_lab_group.id)
        if group is None:
            continue
        members: list[GroupMember] = cast(typ=list[GroupMember], val=group.members.list(all=True))
        for member in members:
            all_members.add(member)
    member_dicts: list[GitLabUserTypedDict] = [project.asdict() for project in list(all_members)]
    for member_dict in member_dicts:
        member_id: int | None = member_dict.get("id")
        if member_id is None:
            continue
        git_lab_user: GitLabUser = GitLabUser.objects.get_or_create(id=member_id)[0]
        git_lab_user.avatar_url = member_dict.get("avatar_url")
        git_lab_user.created_at = convert_and_enforce_utc_timezone(datetime_string=member_dict.get("created_at"))
        git_lab_user.expires_at = convert_and_enforce_utc_timezone(datetime_string=member_dict.get("expires_at"))
        git_lab_user.locked = member_dict.get("locked")
        git_lab_user.membership_state = member_dict.get("membership_state")
        git_lab_user.name = member_dict.get("name")
        git_lab_user.username = member_dict.get("username")
        git_lab_user.web_url = member_dict.get("web_url")
        git_lab_user.save()
    return JsonResponse(data=member_dicts, safe=False)
