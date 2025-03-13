from typing import cast

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab, GitlabListError
from gitlab.v4.objects import Group, GroupMemberAll

from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import convert_and_enforce_utc_timezone
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.models.common.typed_dicts.git_lab_user_typed_dict import GitLabUserTypedDict
from git_lab.models.git_lab_group import GitLabGroup
from git_lab.models.git_lab_user import GitLabUser


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
    all_members: set[GroupMemberAll] = set()
    for git_lab_group in git_lab_groups:
        try:
            group: Group | None = git_lab_client.groups.get(id=git_lab_group.id)
            if group is None:
                continue
            members: list[GroupMemberAll] = cast(
                typ=list[GroupMemberAll],
                val=group.members_all.list(get_all=True)
            )
        except GitlabListError as error:
            print(f"GitLabListError on {git_lab_group.full_path}: {error.error_message}")
            continue
        all_members.update(members)
    member_dicts: list[GitLabUserTypedDict] = [project.asdict() for project in list(all_members)]
    for member_dict in member_dicts:
        member_id: int | None = member_dict.get("id")
        if member_id is None:
            continue
        get_or_create_tuple: tuple[GitLabUser, bool] = GitLabUser.objects.get_or_create(id=member_id)
        git_lab_user: GitLabUser = get_or_create_tuple[0]
        git_lab_user.avatar_url = member_dict.get("avatar_url")
        git_lab_user.locked = member_dict.get("locked") or False
        git_lab_user.name = member_dict.get("name")
        git_lab_user.state = member_dict.get("membership_state")
        git_lab_user.username = member_dict.get("username")
        git_lab_user.web_url = member_dict.get("web_url")
        git_lab_user.created_at = convert_and_enforce_utc_timezone(datetime_string=member_dict.get("created_at"))
        git_lab_user.expires_at = convert_and_enforce_utc_timezone(datetime_string=member_dict.get("expires_at"))
        git_lab_user.save()
    return JsonResponse(data=member_dicts, safe=False)
