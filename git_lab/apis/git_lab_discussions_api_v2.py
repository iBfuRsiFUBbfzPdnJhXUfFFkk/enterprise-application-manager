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
    git_lab_projects: QuerySet[GitLabProject] = cast_query_set(
        typ=GitLabProject,
        val=GitLabProject.objects.filter(~Q(should_skip=True))
    )
    for git_lab_project in iter(git_lab_projects.all()):
        project_dict: GitLabProjectTypedDict = git_lab_project.asdict()
        if DEBUG is True:
            print(f"Processing PROJECT: {project_dict.get("web_url")}")
        project_id: int = git_lab_project.id
        project: Project | None = git_lab_client.projects.get(id=project_id, lazy=False)
        if project is None:
            continue
        project_merge_request_generator: RESTObjectList = project.mergerequests.list(
            iterator=True,
            state="all",
            order_by="created_at",
            sort="desc",
            created_after=one_month_ago,
        )
        for project_merge_request in project_merge_request_generator:
            project_merge_request: ProjectMergeRequest = cast(
                typ=ProjectMergeRequest,
                val=project_merge_request,
            )
            merge_request_dict: GitLabMergeRequestTypedDict = project_merge_request.asdict()
            if DEBUG is True:
                print(f"----Processing MERGE REQUEST: {merge_request_dict.get('web_url')}")
            discussion_generator: RESTObjectList = project_merge_request.discussions.list(
                iterator=True,
            )
            for discussion in discussion_generator:
                discussion_dict: GitLabDiscussionTypedDict = discussion.asdict()
                if DEBUG is True:
                    print(f"--------Processing DISCUSSION: {discussion_dict.get("id")}")
                for note in iter(discussion_dict.get("notes")):
                    if DEBUG is True:
                        print(f"------------Processing NOTE: {note.get("id")}")
    return JsonResponse(
        data={},
        safe=False
    )
