from typing import TypedDict

from core.views.this_api.this_api_sync_git_lab_view.common.models.git_lab_api_user import GitLabApiUser


class GitLabApiNote(TypedDict):
    author: GitLabApiUser | None
    system: bool | None