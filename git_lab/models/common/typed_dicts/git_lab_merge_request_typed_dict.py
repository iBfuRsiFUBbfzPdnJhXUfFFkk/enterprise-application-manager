from typing import TypedDict

from git_lab.models.common.typed_dicts.git_lab_references_typed_dict import GitLabReferencesTypedDict
from git_lab.models.common.typed_dicts.git_lab_task_completion_status_typed_dict import \
    GitLabTaskCompletionStatusTypedDict
from git_lab.models.common.typed_dicts.git_lab_time_stats_typed_dict import GitLabTimeStatsTypedDict
from git_lab.models.common.typed_dicts.git_lab_user_reference_typed_dict import GitLabUserReferenceTypedDict


class GitLabMergeRequestTypedDict(TypedDict):
    assignee: GitLabUserReferenceTypedDict | None
    assignees: list[GitLabUserReferenceTypedDict] | None
    author: GitLabUserReferenceTypedDict | None
    blocking_discussions_resolved: bool | None
    closed_at: str | None
    created_at: str | None
    description: str | None
    draft: bool | None
    has_conflicts: bool | None
    id: int | None
    iid: int | None
    merged_at: str | None
    merged_by: GitLabUserReferenceTypedDict | None
    merged_user: GitLabUserReferenceTypedDict | None
    prepared_at: str | None
    project_id: int | None
    reference: str | None
    references: GitLabReferencesTypedDict | None
    reviewers: list[GitLabUserReferenceTypedDict] | None
    sha: str | None
    source_branch: str | None
    state: str | None
    target_branch: str | None
    task_completion_status: GitLabTaskCompletionStatusTypedDict | None
    time_stats: GitLabTimeStatsTypedDict | None
    title: str | None
    updated_at: str | None
    web_url: str | None
