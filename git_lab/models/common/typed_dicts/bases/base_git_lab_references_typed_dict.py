from typing import TypedDict

from git_lab.models.common.typed_dicts.git_lab_references_typed_dict import GitLabReferencesTypedDict


class BaseGitLabReferencesTypedDict(TypedDict):
    references: GitLabReferencesTypedDict | None
