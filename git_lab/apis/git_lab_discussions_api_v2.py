from datetime import datetime
from typing import cast

from dateutil.relativedelta import relativedelta
from django.db.models import QuerySet, Q
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab
from gitlab.base import RESTObjectList
from gitlab.v4.objects import ProjectMergeRequest, Project

from core.settings.common.developer import DEBUG
from core.utilities.cast_query_set import cast_query_set
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.models.common.typed_dicts.git_lab_discussion_typed_dict import GitLabDiscussionTypedDict
from git_lab.models.common.typed_dicts.git_lab_merge_request_typed_dict import GitLabMergeRequestTypedDict
from git_lab.models.common.typed_dicts.git_lab_note_typed_dict import GitLabNoteTypedDict
from git_lab.models.common.typed_dicts.git_lab_project_typed_dict import GitLabProjectTypedDict
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
                for note_dict in iter(note_dicts):
                    note: GitLabNoteTypedDict = note_dict
                    is_system_note: bool | None = note.get("system")
                    if is_system_note:
                        continue
                    if DEBUG is True:
                        print(f"------------N: {note.get("id")}")
                        print(f"------------N: {note.get("author").get('name')}")
                        print(f"------------N: {note.get("author").get('username')}")
                        print(f"------------N: {note.get("body")}")
    return JsonResponse(
        data={},
        safe=False
    )
