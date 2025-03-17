from typing import TypedDict

from git_lab.models.common.typed_dicts.git_lab_user_reference_typed_dict import GitLabUserReferenceTypedDict


class BaseGitLabAuthorTypedDict(TypedDict):
    author: GitLabUserReferenceTypedDict | None
