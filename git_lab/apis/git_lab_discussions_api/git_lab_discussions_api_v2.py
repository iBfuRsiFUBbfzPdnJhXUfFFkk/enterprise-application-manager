from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.db.models import QuerySet, Q
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab
from gitlab.base import RESTObjectList
from gitlab.v4.objects import Project

from core.settings.common.developer import DEBUG
from core.utilities.cast_query_set import cast_query_set
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.apis.git_lab_discussions_api.git_lab_discussions_api_process_note import \
    git_lab_discussions_api_process_note
from git_lab.models.common.typed_dicts.git_lab_discussion_typed_dict import GitLabDiscussionTypedDict
from git_lab.models.common.typed_dicts.git_lab_merge_request_typed_dict import GitLabMergeRequestTypedDict
from git_lab.models.common.typed_dicts.git_lab_note_typed_dict import GitLabNoteTypedDict
from git_lab.models.git_lab_discussion import GitLabDiscussion
from git_lab.models.git_lab_merge_request import GitLabMergeRequest
from git_lab.models.git_lab_project import GitLabProject


def git_lab_discussions_api_v2(
        request: HttpRequest,
) -> JsonResponse | HttpResponse:
    now: datetime = datetime.now()
    one_month_ago: datetime = now - relativedelta(months=1)
    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        return generic_500(request=request)
    project_models: QuerySet[GitLabProject] = cast_query_set(
        typ=GitLabProject,
        val=GitLabProject.objects.filter(~Q(should_skip=True))
    )
    for project_model in iter(project_models.all()):
        if DEBUG is True:
            print(f"Processing PROJECT: {project_model.web_url}")
        project_id: int = project_model.id
        project_rest_object: Project | None = git_lab_client.projects.get(id=project_id, lazy=False)
        if project_rest_object is None:
            continue
        project_merge_request_generator: RESTObjectList = project_rest_object.mergerequests.list(
            iterator=True,
            state="all",
            order_by="created_at",
            sort="desc",
            created_after=one_month_ago,
        )
        for project_merge_request_rest_object in project_merge_request_generator:
            merge_request_dict: GitLabMergeRequestTypedDict = project_merge_request_rest_object.asdict()
            if DEBUG is True:
                print(f"----M: {merge_request_dict.get('web_url')}")
            discussion_generator: RESTObjectList = project_merge_request_rest_object.discussions.list(
                iterator=True,
            )
            for discussion in discussion_generator:
                discussion_dict: GitLabDiscussionTypedDict = discussion.asdict()
                if DEBUG is True:
                    print(f"--------D: {discussion_dict.get("id")}")
                note_dicts: list[GitLabNoteTypedDict] | None = discussion_dict.get("notes")
                if note_dicts is None:
                    continue
                for index, note_dict in enumerate(iter(note_dicts)):
                    note_dict: GitLabNoteTypedDict = note_dict
                    git_lab_discussions_api_process_note(
                        model_merge_request=GitLabMergeRequest.objects.filter(id=merge_request_dict.get("id")).first(),
                        git_lab_discussion=GitLabDiscussion.objects.filter(id=discussion_dict.get("id")).first(),
                        index=index,
                        note_dict=note_dict,
                    )
    return JsonResponse(
        data={},
        safe=False
    )
