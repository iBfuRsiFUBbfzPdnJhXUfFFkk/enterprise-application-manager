def parse_diff(diff_text: str | None = None) -> tuple[int, int] | None:
    if diff_text is None:
        return None
    additions: int = 0
    removals: int = 0

    for line in diff_text.splitlines():
        if line.startswith('+'):
            additions += 1
        elif line.startswith('-'):
            removals += 1
    return additions, removals
