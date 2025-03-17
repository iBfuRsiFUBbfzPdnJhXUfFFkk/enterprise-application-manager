from git_lab.models.common.typed_dicts.bases.base_git_lab_state_typed_dict import BaseGitLabStateTypedDict
from git_lab.models.common.typed_dicts.bases.git_lab_user_base_typed_dict import GitLabUserBaseTypedDict


class GitLabUserReferenceTypedDict(
    BaseGitLabStateTypedDict,
    GitLabUserBaseTypedDict,
):
    pass
