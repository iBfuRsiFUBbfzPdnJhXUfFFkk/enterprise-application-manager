from typing import TypeVar

from django.db.models import Model

from git_lab.models.common.typed_dicts.bases.base_git_lab_task_completion_status_typed_dict import \
    BaseGitLabTaskCompletionStatusTypedDict
from git_lab.models.common.typed_dicts.git_lab_task_completion_status_typed_dict import \
    GitLabTaskCompletionStatusTypedDict

T = TypeVar("T", bound=Model)
U = TypeVar("U", bound=BaseGitLabTaskCompletionStatusTypedDict)


def task_completion_status_to_model(
        model: T,
        typed_dict: U,
) -> T:
    task_completion_status: GitLabTaskCompletionStatusTypedDict | None = typed_dict.get("task_completion_status")
    if task_completion_status is None:
        return model
    model.task_completion_status_completed_count = task_completion_status.get("completed_count") or 0
    model.task_completion_status_count = task_completion_status.get("count") or 0
    return model
