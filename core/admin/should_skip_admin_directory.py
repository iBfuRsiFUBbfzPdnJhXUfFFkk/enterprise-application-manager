def should_skip_admin_directory(
        exclude_strings: list[str] | None = None,
        root_directory: str | None = None,
):
    if root_directory is None:
        return True
    if exclude_strings is None:
        exclude_strings = []
    for exclude_string in exclude_strings:
        if exclude_string in root_directory:
            return True
    return False
