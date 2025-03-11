from typing import TypedDict

from git_lab.models.common.typed_dicts.git_lab_references_typed_dict import GitLabReferencesTypedDict
from git_lab.models.common.typed_dicts.git_lab_task_completion_status_typed_dict import \
    GitLabTaskCompletionStatusTypedDict
from git_lab.models.common.typed_dicts.git_lab_time_stats_typed_dict import GitLabTimeStatsTypedDict
from git_lab.models.common.typed_dicts.git_lab_user_reference_typed_dict import GitLabUserReferenceTypedDict


class GitLabChangeTypedDict(TypedDict):
    a_mode: str | None
    b_mode: str | None
    deleted_file: bool | None
    diff: str | None
    generated_file: bool | None
    new_file: bool | None
    new_path: str | None
    old_path: str | None
    renamed_file: bool | None

class GitLabMergeRequestChangeDiffRefsTypedDict(TypedDict):
    base_sha: str | None
    head_sha: str | None
    start_sha: str | None

class GitLabMergeRequestChangesTypedDict(TypedDict):
    assignees: list[GitLabUserReferenceTypedDict] | None
    author: GitLabUserReferenceTypedDict | None
    changes: list[GitLabChangeTypedDict] | None
    changes_count: str | None
    closed_by: GitLabUserReferenceTypedDict | None
    created_at: str | None
    description: str | None
    diff_refs: GitLabMergeRequestChangeDiffRefsTypedDict | None
    draft: bool | None
    has_conflicts: bool | None
    id: int
    iid: int | None
    latest_build_finished_at: str | None
    latest_build_started_at: str | None
    merge_commit_sha: str | None
    merged_at: str | None
    merged_by: GitLabUserReferenceTypedDict | None
    prepared_at: str | None
    project_id: int | None
    references: GitLabReferencesTypedDict | None
    sha: str | None
    squash_commit_sha: str | None
    state: str | None
    task_completion_status: GitLabTaskCompletionStatusTypedDict | None
    time_stats: GitLabTimeStatsTypedDict | None
    title: str | None
    updated_at: str | None
    web_url: str | None
