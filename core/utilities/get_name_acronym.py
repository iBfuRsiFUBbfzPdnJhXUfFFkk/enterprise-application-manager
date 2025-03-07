from kpi.utilities.string_or_na import string_or_na


def get_name_acronym(
        acronym: str | None = None,
        name: str | None = None,
) -> str:
    return string_or_na(name) + (f" ({acronym})" if acronym else "")
