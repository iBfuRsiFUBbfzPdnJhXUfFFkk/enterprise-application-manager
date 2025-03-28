from git_lab.models.common.typed_dicts.bases.base_git_lab_assignees_typed_dict import BaseGitLabAssigneesTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_author_typed_dict import BaseGitLabAuthorTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_closed_at_typed_dict import BaseGitLabClosedAtTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_closed_by_typed_dict import BaseGitLabClosedByTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_created_at_typed_dict import BaseGitLabCreatedAtTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_description_typed_dict import BaseGitLabDescriptionTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_id_typed_dict import BaseGitLabIdTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_internal_id_typed_dict import BaseGitLabInternalIdTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_links_typed_dict import BaseGitLabLinksTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_project_id_typed_dict import BaseGitLabProjectIdTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_references_typed_dict import BaseGitLabReferencesTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_state_typed_dict import BaseGitLabStateTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_task_completion_status_typed_dict import \
    BaseGitLabTaskCompletionStatusTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_time_stats_typed_dict import BaseGitLabTimeStatsTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_title_typed_dict import BaseGitLabTitleTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_type_typed_dict import BaseGitLabTypeTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_updated_at_typed_dict import BaseGitLabUpdatedAtTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_web_url_typed_dict import BaseGitLabWebUrlTypedDict
from git_lab.models.common.typed_dicts.git_lab_iteration_typed_dict import GitLabIterationTypedDict


class GitLabIssueTypedDict(
    BaseGitLabAssigneesTypedDict,
    BaseGitLabAuthorTypedDict,
    BaseGitLabClosedAtTypedDict,
    BaseGitLabClosedByTypedDict,
    BaseGitLabCreatedAtTypedDict,
    BaseGitLabDescriptionTypedDict,
    BaseGitLabIdTypedDict,
    BaseGitLabInternalIdTypedDict,
    BaseGitLabLinksTypedDict,
    BaseGitLabProjectIdTypedDict,
    BaseGitLabReferencesTypedDict,
    BaseGitLabStateTypedDict,
    BaseGitLabTaskCompletionStatusTypedDict,
    BaseGitLabTimeStatsTypedDict,
    BaseGitLabTitleTypedDict,
    BaseGitLabTypeTypedDict,
    BaseGitLabUpdatedAtTypedDict,
    BaseGitLabWebUrlTypedDict,
):
    blocking_issues_count: int | None
    has_tasks: bool | None
    issue_type: str | None
    iteration: GitLabIterationTypedDict | None
    user_notes_count: int | None
    weight: int | None
