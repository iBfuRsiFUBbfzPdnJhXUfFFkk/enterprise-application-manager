from git_lab.models.common.typed_dicts.bases.base_git_lab_avatar_url_typed_dict import BaseGitLabAvatarUrlTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_created_at_typed_dict import BaseGitLabCreatedAtTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_description_typed_dict import BaseGitLabDescriptionTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_id_typed_dict import BaseGitLabIdTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_links_typed_dict import BaseGitLabLinksTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_name_typed_dict import BaseGitLabNameTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_path_typed_dict import BaseGitLabPathTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_updated_at_typed_dict import BaseGitLabUpdatedAtTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_web_url_typed_dict import BaseGitLabWebUrlTypedDict
from git_lab.models.common.typed_dicts.git_lab_namespace_typed_dict import GitLabNamespaceTypedDict


class GitLabProjectTypedDict(
    BaseGitLabAvatarUrlTypedDict,
    BaseGitLabCreatedAtTypedDict,
    BaseGitLabDescriptionTypedDict,
    BaseGitLabIdTypedDict,
    BaseGitLabLinksTypedDict,
    BaseGitLabNameTypedDict,
    BaseGitLabPathTypedDict,
    BaseGitLabUpdatedAtTypedDict,
    BaseGitLabWebUrlTypedDict,
):
    container_registry_image_prefix: str | None
    default_branch: str | None
    http_url_to_repo: str | None
    last_activity_at: str | None
    name_with_namespace: str | None
    namespace: GitLabNamespaceTypedDict | None
    open_issues_count: int | None
    path_with_namespace: str | None
    readme_url: str | None
    ssh_url_to_repo: str | None
