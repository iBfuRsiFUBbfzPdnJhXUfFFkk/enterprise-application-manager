from typing import TypeVar

from git_lab.models.common.abstract.abstract_git_lab_state import AbstractGitLabState
from git_lab.models.common.typed_dicts.bases.base_git_lab_state_typed_dict import BaseGitLabStateTypedDict

T = TypeVar("T", bound=AbstractGitLabState)
U = TypeVar("U", bound=BaseGitLabStateTypedDict)


def state_to_model(
        model: T,
        typed_dict: U,
) -> T:
    model.state = typed_dict.get("state")
    return model
