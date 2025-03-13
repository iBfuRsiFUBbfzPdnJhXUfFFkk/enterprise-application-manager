from typing import cast

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab, GitlabListError
from gitlab.v4.objects import ProjectMergeRequest, ProjectMergeRequestDiscussion, Project

from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import convert_and_enforce_utc_timezone
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.apis.common.get_common_query_parameters import GitLabApiCommonQueryParameters, get_common_query_parameters
from git_lab.models.common.typed_dicts.git_lab_discussion_typed_dict import GitLabDiscussionTypedDict
from git_lab.models.common.typed_dicts.git_lab_note_typed_dict import GitLabNoteTypedDict
from git_lab.models.common.typed_dicts.git_lab_user_reference_typed_dict import GitLabUserReferenceTypedDict
from git_lab.models.git_lab_discussion import GitLabDiscussion
from git_lab.models.git_lab_note import GitLabNote
from git_lab.models.git_lab_project import GitLabProject
from git_lab.models.git_lab_user import GitLabUser
from scrum.models.scrum_sprint import ScrumSprint


def git_lab_discussions_api(
        request: HttpRequest,
) -> JsonResponse | HttpResponse:
    query_parameters: GitLabApiCommonQueryParameters = get_common_query_parameters(request=request)
    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        return generic_500(request=request)
    git_lab_projects: QuerySet[GitLabProject] = cast_query_set(
        typ=GitLabProject,
        val=GitLabProject.objects.all()
    )
    all_project_merge_requests: set[ProjectMergeRequest] = set()
    for git_lab_project in git_lab_projects:
        try:
            project_id: int = git_lab_project.id
            project: Project | None = git_lab_client.projects.get(id=project_id, lazy=True)
            if project is None:
                continue
            project_merge_requests: list[ProjectMergeRequest] = cast(
                typ=list[ProjectMergeRequest],
                val=project.mergerequests.list(**query_parameters)
            )
        except GitlabListError as error:
            print(f"GitLabListError on {git_lab_project.name_with_namespace}: {error.error_message}")
            continue
        all_project_merge_requests.update(project_merge_requests)
    all_discussions: set[ProjectMergeRequestDiscussion] = set()
    for project_merge_request in list(all_project_merge_requests):
        discussions: list[ProjectMergeRequestDiscussion] = cast(
            typ=list[ProjectMergeRequestDiscussion],
            val=project_merge_request.discussions.list(**query_parameters)
        )
        all_discussions.update(discussions)
    all_discussion_dicts: list[GitLabDiscussionTypedDict] = [discussion.asdict() for discussion in all_discussions]
    for discussion_dict in all_discussion_dicts:
        discussion_id: str | None = discussion_dict.get("id")
        if discussion_id is None:
            continue
        get_or_create_tuple: tuple[GitLabDiscussion, bool] = GitLabDiscussion.objects.get_or_create(id=discussion_id)
        git_lab_discussion: GitLabDiscussion = get_or_create_tuple[0]
        git_lab_discussion.individual_note = discussion_dict.get("individual_note")
        notes: list[GitLabNoteTypedDict] | None = discussion_dict.get("notes")
        if notes is not None:
            for note in notes:
                note_id: int | None = note.get("id")
                if note_id is None:
                    continue
                get_or_create_tuple: tuple[GitLabNote, bool] = GitLabNote.objects.get_or_create(id=note_id)
                git_lab_note: GitLabNote = get_or_create_tuple[0]
                git_lab_note.body = note.get("body")
                git_lab_note.noteable_id = note.get("noteable_id")
                git_lab_note.noteable_iid = note.get("noteable_iid")
                git_lab_note.noteable_type = note.get("noteable_type")
                git_lab_note.system = note.get("system") or True
                git_lab_note.type = note.get("type")
                git_lab_note.created_at = convert_and_enforce_utc_timezone(datetime_string=note.get("created_at"))
                git_lab_note.updated_at = convert_and_enforce_utc_timezone(datetime_string=note.get("updated_at"))
                git_lab_note.discussion = git_lab_discussion
                author: GitLabUserReferenceTypedDict | None = note.get("author")
                if author is not None:
                    git_lab_note.author = GitLabUser.objects.filter(id=author.get("id")).first()
                project: GitLabProject | None = GitLabProject.objects.filter(id=note.get("project_id")).first()
                if project is not None:
                    git_lab_note.project = project
                    git_lab_discussion.project = project
                    git_lab_note.group = project.group
                    git_lab_discussion.group = project.group
                scrum_sprint: ScrumSprint | None = ScrumSprint.objects.filter(
                    date_start__lte=git_lab_note.created_at,
                    date_end__gte=git_lab_note.created_at,
                ).first()
                if scrum_sprint is not None:
                    git_lab_note.scrum_sprint = scrum_sprint
                    git_lab_discussion.scrum_sprint = scrum_sprint
                git_lab_note.save()
        git_lab_discussion.save()
    return JsonResponse(data=all_discussion_dicts, safe=False)
