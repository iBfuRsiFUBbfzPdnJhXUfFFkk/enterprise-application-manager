from git_lab.models.common.typed_dicts.bases.base_git_lab_author_typed_dict import BaseGitLabAuthorTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_created_at_typed_dict import BaseGitLabCreatedAtTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_id_typed_dict import BaseGitLabIdTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_project_id_typed_dict import BaseGitLabProjectIdTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_type_typed_dict import BaseGitLabTypeTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_updated_at_typed_dict import BaseGitLabUpdatedAtTypedDict


class GitLabNoteTypedDict(
    BaseGitLabAuthorTypedDict,
    BaseGitLabCreatedAtTypedDict,
    BaseGitLabIdTypedDict,
    BaseGitLabProjectIdTypedDict,
    BaseGitLabTypeTypedDict,
    BaseGitLabUpdatedAtTypedDict,
):
    body: str | None
    noteable_id: int | None
    noteable_iid: int | None
    noteable_type: str | None
    system: bool | None
