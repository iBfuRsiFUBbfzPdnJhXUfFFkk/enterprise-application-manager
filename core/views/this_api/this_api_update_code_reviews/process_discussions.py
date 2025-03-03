from core.views.this_api.this_api_update_code_reviews.fetch_discussions_for_pull_requests import NoteEntry, Note


def process_discussions(
        discussions: list[NoteEntry] | None = None,
        usernames_of_approvals: list[str] | None = None,
) -> tuple[int, int] | None:
    count_comment: int = 0
    count_thread: int = 0

    for discussion in discussions:
        notes: list[Note] = discussion.get('notes', [])
        if not notes:
            continue
        first_note: Note = notes[0]
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