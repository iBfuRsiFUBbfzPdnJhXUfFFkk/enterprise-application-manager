def get_name_acronym(acronym: str | None, name: str | None) -> str:
    return f"{name or 'PLEASE ADD NAME'}" + (f" ({acronym})" if acronym else "")
