from gitlab.base import RESTObject
from gitlab.base import RESTObjectList

from core.settings.common.developer import DEBUG
from git_lab.apis.git_lab_discussions_api.git_lab_discussions_api_payload import GitLabDiscussionsApiPayload
from git_lab.apis.git_lab_discussions_api.git_lab_discussions_api_process_discussion import \
    git_lab_discussions_api_process_discussion
from git_lab.models.common.typed_dicts.git_lab_discussion_typed_dict import GitLabDiscussionTypedDict
from git_lab.models.common.typed_dicts.git_lab_merge_request_typed_dict import GitLabMergeRequestTypedDict
from git_lab.models.git_lab_merge_request import GitLabMergeRequest


def git_lab_discussions_api_process_merge_request(
        project_merge_request_rest_object: RESTObject | None = None,
        payload: GitLabDiscussionsApiPayload | None = None,
) -> GitLabDiscussionsApiPayload:
    if payload is None:
        payload: GitLabDiscussionsApiPayload = {}
    if project_merge_request_rest_object is None:
        return payload
    merge_request_dict: GitLabMergeRequestTypedDict = project_merge_request_rest_object.asdict()
    merge_request_id: int = merge_request_dict.get("id")
    web_url: str | None = merge_request_dict.get("web_url")
    if DEBUG is True:
        print(f"----M: {web_url}")
    model_merge_request: GitLabMergeRequest | None = GitLabMergeRequest.objects.filter(id=merge_request_id).first()
    if model_merge_request is None:
        payload["total_number_of_merge_requests_not_synchronized"] += 1
        return payload
    discussion_generator: RESTObjectList = project_merge_request_rest_object.discussions.list(iterator=True)
    for discussion in discussion_generator:
        discussion_dict: GitLabDiscussionTypedDict = discussion.asdict()
        payload: GitLabDiscussionsApiPayload = git_lab_discussions_api_process_discussion(
            discussion_dict=discussion_dict,
            model_merge_request=model_merge_request,
            payload=payload,
        )
    return payload
