def coerce_integer(value: int | float | str | None = None) -> int:
    if value is None:
        return 0
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    try:
        return int(value)
    except ValueError:
        return 0
