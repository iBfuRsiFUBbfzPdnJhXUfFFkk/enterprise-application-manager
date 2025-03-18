from typing import TypeVar

from django.db.models import Model

from git_lab.apis.common.typed_dict_to_model.generic_user_to_model import generic_user_to_model
from git_lab.models.common.typed_dicts.bases.base_git_lab_closed_by_typed_dict import BaseGitLabClosedByTypedDict

T = TypeVar("T", bound=Model)
U = TypeVar("U", bound=BaseGitLabClosedByTypedDict)


def closed_by_to_model(
        model: T,
        typed_dict: U,
) -> T:
    return generic_user_to_model(
        model=model,
        typed_dict=typed_dict,
        user_model_field="closed_by",
    )
