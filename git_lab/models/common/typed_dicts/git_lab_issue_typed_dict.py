from typing import TypedDict

from git_lab.models.common.typed_dicts.git_lab_iteration_typed_dict import GitLabIterationTypedDict
from git_lab.models.common.typed_dicts.git_lab_links_typed_dict import GitLabLinksTypedDict
from git_lab.models.common.typed_dicts.git_lab_references_typed_dict import GitLabReferencesTypedDict
from git_lab.models.common.typed_dicts.git_lab_task_completion_status_typed_dict import \
    GitLabTaskCompletionStatusTypedDict
from git_lab.models.common.typed_dicts.git_lab_time_stats_typed_dict import GitLabTimeStatsTypedDict
from git_lab.models.common.typed_dicts.git_lab_user_reference_typed_dict import GitLabUserReferenceTypedDict


class GitLabIssueTypedDict(TypedDict):
    _links: GitLabLinksTypedDict | None
    assignees: list[GitLabUserReferenceTypedDict] | None
    author: GitLabUserReferenceTypedDict | None
    blocking_issues_count: int | None
    closed_at: str | None
    closed_by: GitLabUserReferenceTypedDict | None
    created_at: str | None
    description: str | None
    has_tasks: bool | None
    id: int
    iid: int | None
    issue_type: str | None
    iteration: GitLabIterationTypedDict | None
    project_id: int | None
    references: GitLabReferencesTypedDict | None
    state: str | None
    task_completion_status: GitLabTaskCompletionStatusTypedDict | None
    time_stats: GitLabTimeStatsTypedDict | None
    title: str | None
    type: str | None
    updated_at: str | None
    user_notes_count: int | None
    web_url: str | None
    weight: int | None