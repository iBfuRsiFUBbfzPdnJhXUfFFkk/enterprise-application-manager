from git_lab.models.common.typed_dicts.git_lab_user_base_typed_dict import GitLabUserBaseTypedDict
from git_lab.models.common.typed_dicts.git_lab_user_reference_typed_dict import GitLabUserReferenceTypedDict


class GitLabUserTypedDict(GitLabUserBaseTypedDict):
    created_at: str | None
    created_by: GitLabUserReferenceTypedDict | None
    expires_at: str | None
    membership_state: str | None
