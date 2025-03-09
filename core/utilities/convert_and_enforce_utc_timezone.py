from datetime import datetime, tzinfo, timezone


def convert_and_enforce_utc_timezone(
        datetime_string: str | None = None,
) -> datetime | None:
    if datetime_string is None:
        return None
    try:
        datetime_object: datetime = datetime.fromisoformat(datetime_string)
    except ValueError:
        return None
    time_zone_info: tzinfo | None = datetime_object.tzinfo
    if time_zone_info is None:
        datetime_object = datetime_object.replace(tzinfo=timezone.utc)
    else:
        datetime_object = datetime_object.astimezone(tz=timezone.utc)
    return datetime_object
