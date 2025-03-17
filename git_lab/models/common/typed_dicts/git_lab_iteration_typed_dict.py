from git_lab.models.common.typed_dicts.bases.base_git_lab_created_at_typed_dict import BaseGitLabCreatedAtTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_description_typed_dict import BaseGitLabDescriptionTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_id_typed_dict import BaseGitLabIdTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_internal_id_typed_dict import BaseGitLabInternalIdTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_state_typed_dict import BaseGitLabStateTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_title_typed_dict import BaseGitLabTitleTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_updated_at_typed_dict import BaseGitLabUpdatedAtTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_web_url_typed_dict import BaseGitLabWebUrlTypedDict


class GitLabIterationTypedDict(
    BaseGitLabCreatedAtTypedDict,
    BaseGitLabDescriptionTypedDict,
    BaseGitLabIdTypedDict,
    BaseGitLabInternalIdTypedDict,
    BaseGitLabStateTypedDict,
    BaseGitLabTitleTypedDict,
    BaseGitLabUpdatedAtTypedDict,
    BaseGitLabWebUrlTypedDict,
):
    due_date: str | None
    group_id: int | None
    sequence: int | None
    start_date: str | None
