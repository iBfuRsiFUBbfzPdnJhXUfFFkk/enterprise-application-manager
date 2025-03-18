from typing import TypeVar

from git_lab.models.common.abstract.abstract_git_lab_title import AbstractGitLabTitle
from git_lab.models.common.typed_dicts.bases.base_git_lab_title_typed_dict import BaseGitLabTitleTypedDict

T = TypeVar("T", bound=AbstractGitLabTitle)
U = TypeVar("U", bound=BaseGitLabTitleTypedDict)


def title_to_model(
        model: T,
        typed_dict: U,
) -> T:
    model.title = typed_dict.get("title")
    return model
