from git_lab.models.common.typed_dicts.git_lab_user_base_typed_dict import GitLabUserBaseTypedDict


class GitLabUserReferenceTypedDict(GitLabUserBaseTypedDict):
    state: str | None
