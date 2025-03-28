from git_lab.models.common.typed_dicts.bases.base_git_lab_avatar_url_typed_dict import BaseGitLabAvatarUrlTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_created_at_typed_dict import BaseGitLabCreatedAtTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_description_typed_dict import BaseGitLabDescriptionTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_id_typed_dict import BaseGitLabIdTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_name_typed_dict import BaseGitLabNameTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_path_typed_dict import BaseGitLabPathTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_web_url_typed_dict import BaseGitLabWebUrlTypedDict


class GitLabGroupTypedDict(
    BaseGitLabAvatarUrlTypedDict,
    BaseGitLabCreatedAtTypedDict,
    BaseGitLabDescriptionTypedDict,
    BaseGitLabIdTypedDict,
    BaseGitLabNameTypedDict,
    BaseGitLabPathTypedDict,
    BaseGitLabWebUrlTypedDict,
):
    full_name: str | None
    full_path: str | None
