from datetime import datetime, UTC

from gitlab.v4.objects import GroupMember

from core.models.person import Person
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import IndicatorMap, ensure_indicator_map, \
    ensure_indicator_is_in_map


def parse_datetime(datetime_str: str | None) -> datetime | None:
    if datetime_str is None:
        return None
    dt: datetime = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.replace(tzinfo=UTC)


def handle_group_member(
        group_member: GroupMember | None = None,
        indicator_map: IndicatorMap | None = None,
) -> IndicatorMap:
    indicator_map: IndicatorMap = ensure_indicator_map(indicator_map=indicator_map)
    if group_member is None:
        return indicator_map
    gitlab_access_level_int: int | None = group_member.access_level
    gitlab_id_int: int | None = group_member.id
    gitlab_id: str | None = str(object=gitlab_id_int) if gitlab_id_int is not None else None
    gitlab_name: str | None = group_member.name
    gitlab_names: list[str] = (gitlab_name or "").split(" ")
    gitlab_username: str | None = group_member.username
    gitlab_first_name: str = gitlab_names[0] if len(gitlab_names) > 0 else ""
    gitlab_last_name: str = gitlab_names[1] if len(gitlab_names) > 1 else ""
    print(f"------------------------------------")
    print(f"gitlab_id: {gitlab_id}")
    print(f"gitlab_name: {gitlab_name}")
    print(f"gitlab_username: {gitlab_username}")
    print(f"------------------------------------")
    indicator_map: IndicatorMap = ensure_indicator_is_in_map(
        git_lab_user_id=gitlab_id,
        indicator_map=indicator_map
    )
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
    person.gitlab_sync_id = gitlab_id
    person.gitlab_sync_is_locked = group_member.locked
    person.gitlab_sync_membership_state = group_member.membership_state
    person.gitlab_sync_name = gitlab_name
    person.gitlab_sync_state = group_member.state
    person.gitlab_sync_username = gitlab_username
    person.gitlab_sync_web_url = group_member.web_url
    person.save()
    return indicator_map
