from typing import TypeVar

from django.db.models import Model

from git_lab.apis.common.typed_dict_to_model.generic_users_to_model import generic_users_to_model
from git_lab.models.common.typed_dicts.bases.base_git_lab_assignees_typed_dict import BaseGitLabAssigneesTypedDict

T = TypeVar("T", bound=Model)
U = TypeVar("U", bound=BaseGitLabAssigneesTypedDict)


def assignees_to_model(
        model: T,
        typed_dict: U,
) -> T:
    return generic_users_to_model(
        model=model,
        typed_dict=typed_dict,
        users_model_field="assignees",
    )
