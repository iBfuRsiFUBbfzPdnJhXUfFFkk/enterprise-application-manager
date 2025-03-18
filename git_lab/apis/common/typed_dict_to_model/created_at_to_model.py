from typing import TypeVar

from core.utilities.convert_and_enforce_utc_timezone import convert_and_enforce_utc_timezone
from git_lab.models.common.abstract.abstract_git_lab_created_at import AbstractGitLabCreatedAt
from git_lab.models.common.typed_dicts.bases.base_git_lab_created_at_typed_dict import BaseGitLabCreatedAtTypedDict

T = TypeVar("T", bound=AbstractGitLabCreatedAt)
U = TypeVar("U", bound=BaseGitLabCreatedAtTypedDict)


def created_at_to_model(
        model: T,
        typed_dict: U,
) -> T:
    model.created_at = convert_and_enforce_utc_timezone(
        datetime_string=typed_dict.get("created_at")
    )
    return model
