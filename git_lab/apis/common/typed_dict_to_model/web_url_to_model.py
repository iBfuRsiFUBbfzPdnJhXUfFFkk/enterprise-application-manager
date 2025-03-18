from typing import TypeVar

from git_lab.models.common.abstract.abstract_git_lab_web_url import AbstractGitLabWebUrl
from git_lab.models.common.typed_dicts.bases.base_git_lab_web_url_typed_dict import BaseGitLabWebUrlTypedDict

T = TypeVar("T", bound=AbstractGitLabWebUrl)
U = TypeVar("U", bound=BaseGitLabWebUrlTypedDict)


def web_url_to_model(
        model: T,
        typed_dict: U,
) -> T:
    model.web_url = typed_dict.get("web_url")
    return model
