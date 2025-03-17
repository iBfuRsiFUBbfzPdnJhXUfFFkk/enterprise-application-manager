from git_lab.models.common.typed_dicts.bases.base_git_lab_created_at_typed_dict import BaseGitLabCreatedAtTypedDict
from git_lab.models.common.typed_dicts.bases.git_lab_user_base_typed_dict import GitLabUserBaseTypedDict
from git_lab.models.common.typed_dicts.git_lab_user_reference_typed_dict import GitLabUserReferenceTypedDict


class GitLabUserTypedDict(
    GitLabUserBaseTypedDict,
    BaseGitLabCreatedAtTypedDict,
):
    created_by: GitLabUserReferenceTypedDict | None
    expires_at: str | None
    membership_state: str | None
