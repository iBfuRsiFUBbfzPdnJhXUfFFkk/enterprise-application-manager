from git_lab.models.common.typed_dicts.bases.base_git_lab_closed_at_typed_dict import BaseGitLabClosedAtTypedDict
from git_lab.models.common.typed_dicts.bases.base_git_lab_merge_request_typed_dict import \
    BaseGitLabMergeRequestTypedDict
from git_lab.models.common.typed_dicts.git_lab_user_reference_typed_dict import GitLabUserReferenceTypedDict


class GitLabMergeRequestTypedDict(
    BaseGitLabClosedAtTypedDict,
    BaseGitLabMergeRequestTypedDict,
):
    blocking_discussions_resolved: bool | None
    merged_user: GitLabUserReferenceTypedDict | None
    reference: str | None
    reviewers: list[GitLabUserReferenceTypedDict] | None
    source_branch: str | None
    target_branch: str | None
