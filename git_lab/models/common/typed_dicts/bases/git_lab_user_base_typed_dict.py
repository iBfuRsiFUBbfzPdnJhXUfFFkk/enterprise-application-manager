from git_lab.models.common.typed_dicts.bases.base_git_lab_avatar_url_typed_dict import BaseGitLabAvatarUrlTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_id_typed_dict import BaseGitLabIdTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_name_typed_dict import BaseGitLabNameTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_web_url_typed_dict import BaseGitLabWebUrlTypedDict


class GitLabUserBaseTypedDict(
    BaseGitLabAvatarUrlTypedDict,
    BaseGitLabIdTypedDict,
    BaseGitLabNameTypedDict,
    BaseGitLabWebUrlTypedDict,
):
    locked: bool | None
    username: str | None
