from kpi.utilities.coerce_float import coerce_float


def safe_divide(
        dividend: float | int | str | None = None,
        divisor: float | int | str | None = None,
) -> float:
    dividend: float = coerce_float(value=dividend)
    divisor: float = coerce_float(value=divisor)
    if divisor == 0:
        return 0
    try:
        return dividend / divisor
    except ZeroDivisionError:
        return 0
