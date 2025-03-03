def process_discussions(
        discussions: list[dict] | None = None,
        usernames_of_approvals: list[str] | None = None,
) -> tuple[int, int] | None:
    count_comment: int = 0
    count_thread: int = 0

    for discussion in discussions:
        notes = discussion.get('notes', [])
        if not notes:
            continue
        first_note = notes[0]
        if not first_note.get("system"):
            first_author = first_note.get("author", {}).get("username")
            if first_author in usernames_of_approvals:
                count_thread += 1

        for note in notes:
            if note.get("system"):
                continue
            note_author = note.get("author", {}).get("username")
            if note_author in usernames_of_approvals:
                count_comment += 1
    return count_comment, count_thread