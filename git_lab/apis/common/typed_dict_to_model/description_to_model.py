from typing import TypeVar

from git_lab.models.common.abstract.abstract_git_lab_description import AbstractGitLabDescription
from git_lab.models.common.typed_dicts.bases.base_git_lab_description_typed_dict import BaseGitLabDescriptionTypedDict

T = TypeVar("T", bound=AbstractGitLabDescription)
U = TypeVar("U", bound=BaseGitLabDescriptionTypedDict)


def description_to_model(
        model: T,
        typed_dict: U,
) -> T:
    model.description = typed_dict.get("description")
    return model
