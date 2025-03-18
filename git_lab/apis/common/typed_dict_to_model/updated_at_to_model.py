from typing import TypeVar

from core.utilities.convert_and_enforce_utc_timezone import convert_and_enforce_utc_timezone
from git_lab.models.common.abstract.abstract_git_lab_updated_at import AbstractGitLabUpdatedAt
from git_lab.models.common.typed_dicts.bases.base_git_lab_updated_at_typed_dict import BaseGitLabUpdatedAtTypedDict

T = TypeVar("T", bound=AbstractGitLabUpdatedAt)
U = TypeVar("U", bound=BaseGitLabUpdatedAtTypedDict)


def updated_at_to_model(
        model: T,
        typed_dict: U,
) -> T:
    model.updated_at = convert_and_enforce_utc_timezone(
        datetime_string=typed_dict.get("updated_at")
    )
    return model
