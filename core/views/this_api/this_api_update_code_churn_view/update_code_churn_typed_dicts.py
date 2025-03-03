from typing import TypedDict, Optional, List


class User(TypedDict, total=False):
    avatar_url: Optional[str]
    id: Optional[int]
    locked: Optional[bool]
    name: Optional[str]
    state: Optional[str]
    username: Optional[str]
    web_url: Optional[str]


class Milestone(TypedDict, total=False):
    created_at: Optional[str]
    description: Optional[str]
    due_date: Optional[str]
    id: Optional[int]
    iid: Optional[int]
    project_id: Optional[int]
    start_date: Optional[str]
    state: Optional[str]
    title: Optional[str]
    updated_at: Optional[str]
    web_url: Optional[str]


class References(TypedDict, total=False):
    full: Optional[str]
    relative: Optional[str]
    short: Optional[str]


class TimeStats(TypedDict, total=False):
    human_time_estimate: Optional[str]
    human_total_time_spent: Optional[str]
    time_estimate: Optional[int]
    total_time_spent: Optional[int]


class TaskCompletionStatus(TypedDict, total=False):
    completed_count: Optional[int]
    count: Optional[int]


class MergeRequest(TypedDict, total=False):
    approvals_before_merge: Optional[int]
    assignee: Optional[User]
    assignees: Optional[List[User]]
    author: Optional[User]
    blocking_discussions_resolved: Optional[bool]
    closed_at: Optional[str]
    closed_by: Optional[str]
    created_at: Optional[str]
    description: Optional[str]
    detailed_merge_status: Optional[str]
    discussion_locked: Optional[bool]
    downvotes: Optional[int]
    draft: Optional[bool]
    force_remove_source_branch: Optional[bool]
    has_conflicts: Optional[bool]
    id: Optional[int]
    iid: Optional[int]
    imported: Optional[bool]
    imported_from: Optional[str]
    labels: Optional[List[str]]
    merge_after: Optional[str]
    merge_commit_sha: Optional[str]
    merge_status: Optional[str]
    merge_user: Optional[User]
    merge_when_pipeline_succeeds: Optional[bool]
    merged_at: Optional[str]
    merged_by: Optional[User]
    milestone: Optional[Milestone]
    prepared_at: Optional[str]
    project_id: Optional[int]
    reference: Optional[str]
    references: Optional[References]
    reviewers: Optional[List[User]]
    sha: Optional[str]
    should_remove_source_branch: Optional[bool]
    source_branch: Optional[str]
    source_project_id: Optional[int]
    squash: Optional[bool]
    squash_commit_sha: Optional[str]
    squash_on_merge: Optional[bool]
    state: Optional[str]
    target_branch: Optional[str]
    target_project_id: Optional[int]
    task_completion_status: Optional[TaskCompletionStatus]
    time_stats: Optional[TimeStats]
    title: Optional[str]
    updated_at: Optional[str]
    upvotes: Optional[int]
    user_notes_count: Optional[int]
    web_url: Optional[str]
    work_in_progress: Optional[bool]


class Change(TypedDict):
    a_mode: str | None
    b_mode: str | None
    diff: str | None
    new_path: str | None
    old_path: str | None


class Changes(TypedDict):
    changes: List[Change] | None
