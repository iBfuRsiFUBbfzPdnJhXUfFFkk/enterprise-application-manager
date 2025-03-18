from git_lab.apis.common.typed_dict_to_model.group_merge_request_to_model import group_merge_request_to_model
from git_lab.models.common.typed_dicts.git_lab_merge_request_typed_dict import GitLabMergeRequestTypedDict
from git_lab.models.git_lab_merge_request import GitLabMergeRequest


def git_lab_merge_requests_api_process_merge_request(
        merge_request_dict: GitLabMergeRequestTypedDict,
) -> GitLabMergeRequest | None:
    instance: GitLabMergeRequest | None = group_merge_request_to_model(typed_dict=merge_request_dict)
    if instance is None:
        return None
    instance.save()
    return instance
