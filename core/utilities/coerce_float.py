def coerce_float(value: int | float | str | None = None) -> float:
    if value is None:
        return 0.0
    if isinstance(value, float):
        return value
    if isinstance(value, int):
        return float(value)
    try:
        return float(value)
    except ValueError:
        return 0.0
