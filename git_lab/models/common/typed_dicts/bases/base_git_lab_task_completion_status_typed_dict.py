from typing import TypedDict

from git_lab.models.common.typed_dicts.git_lab_task_completion_status_typed_dict import \
    GitLabTaskCompletionStatusTypedDict


class BaseGitLabTaskCompletionStatusTypedDict(TypedDict):
    task_completion_status: GitLabTaskCompletionStatusTypedDict | None
