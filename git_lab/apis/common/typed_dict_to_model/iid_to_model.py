from typing import TypeVar

from git_lab.models.common.abstract.abstract_git_lab_internal_identification import AbstractGitLabInternalIdentification
from git_lab.models.common.typed_dicts.bases.base_git_lab_internal_id_typed_dict import BaseGitLabInternalIdTypedDict

T = TypeVar("T", bound=AbstractGitLabInternalIdentification)
U = TypeVar("U", bound=BaseGitLabInternalIdTypedDict)


def iid_to_model(
        model: T,
        typed_dict: U,
) -> T:
    model.iid = typed_dict.get("iid")
    return model
