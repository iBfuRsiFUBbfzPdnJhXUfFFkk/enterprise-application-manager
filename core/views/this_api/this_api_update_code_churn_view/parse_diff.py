def parse_diff(diff_text: str | None = None) -> tuple[int, int] | None:
    if diff_text is None:
        return None
    additions = 0
    removals = 0

    for line in diff_text.splitlines():
        if line.startswith("@@") or line.startswith(" "):
            continue
        if line.startswith('+'):
            additions += 1
        elif line.startswith('-'):
            removals += 1
    return additions, removals
