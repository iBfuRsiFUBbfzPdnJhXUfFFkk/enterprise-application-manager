from git_lab.models.common.typed_dicts.bases.base_git_lab_merge_request_typed_dict import \
    BaseGitLabMergeRequestTypedDict
from git_lab.models.common.typed_dicts.git_lab_merge_request_change_diff_refs_typed_dict import \
    GitLabMergeRequestChangeDiffRefsTypedDict


class GitLabMergeRequestChangesTypedDict(
    BaseGitLabMergeRequestTypedDict,
):
    changes_count: str | None
    diff_refs: GitLabMergeRequestChangeDiffRefsTypedDict | None
    latest_build_finished_at: str | None
    latest_build_started_at: str | None
    merge_commit_sha: str | None
    squash_commit_sha: str | None
