from datetime import datetime, timezone
from typing import cast

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab, GitlabListError
from gitlab.v4.objects import ProjectMergeRequest, ProjectMergeRequestDiscussion

from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import convert_and_enforce_utc_timezone
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.models.common.typed_dicts.git_lab_discussion_typed_dict import GitLabDiscussionTypedDict
from git_lab.models.common.typed_dicts.git_lab_note_typed_dict import GitLabNoteTypedDict
from git_lab.models.git_lab_discussion import GitLabDiscussion
from git_lab.models.git_lab_note import GitLabNote
from git_lab.models.git_lab_project import GitLabProject


def git_lab_discussions_api(
        request: HttpRequest,
) -> JsonResponse | HttpResponse:
    all_parameter: bool = request.GET.get('all', True)
    page: int | None = request.GET.get('page', None)
    per_page: int | None = request.GET.get('per_page', None)
    author_id: int | None = request.GET.get('author_id', None)
    assignee_id: int | None = request.GET.get('assignee_id', None)
    iteration_id: int | None = request.GET.get('iteration_id', None)
    state: str = request.GET.get('state', "all")
    created_before: str | None = request.GET.get('created_before', None)
    created_after: str | None = request.GET.get('created_after', None)
    updated_after: str | None = request.GET.get('updated_after', None)
    updated_before: str | None = request.GET.get('updated_before', None)
    created_before_dt: datetime | None = None
    created_after_dt: datetime | None = None
    updated_after_dt: datetime | None = None
    updated_before_dt: datetime | None = None
    if created_before is not None:
        created_before_dt = datetime.strptime(created_before, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    if created_after is not None:
        created_after_dt = datetime.strptime(created_after, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    if updated_after is not None:
        updated_after_dt = datetime.strptime(updated_after, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    if updated_before is not None:
        updated_before_dt = datetime.strptime(updated_before, "%Y-%m-%d").replace(tzinfo=timezone.utc)
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
            project_merge_requests: list[ProjectMergeRequest] | None = git_lab_client.projects.get(
                id=git_lab_project.id, lazy=True
            ).mergerequests.list(
                all=all_parameter,
                assignee_id=assignee_id,
                author_id=author_id,
                created_after=created_after_dt,
                created_before=created_before_dt,
                iteration_id=iteration_id,
                page=page,
                per_page=per_page,
                state=state,
                updated_after=updated_after_dt,
                updated_before=updated_before_dt,
            )
        except GitlabListError as error:
            print(f"GitLabListError on {git_lab_project.name_with_namespace}: {error.error_message}")
            continue
        if project_merge_requests is None:
            continue
        for project_merge_request in project_merge_requests:
            all_project_merge_requests.add(project_merge_request)
    all_discussions: set[ProjectMergeRequestDiscussion] = set()
    for project_merge_request in list(all_project_merge_requests):
        discussions: list[ProjectMergeRequestDiscussion] = cast(
            typ=list[ProjectMergeRequestDiscussion],
            val=project_merge_request.discussions.list(all=True)
        )
        for discussion in discussions:
            all_discussions.add(discussion)
    all_discussion_dicts: list[GitLabDiscussionTypedDict] = [discussion.asdict() for discussion in all_discussions]
    for discussion_dict in all_discussion_dicts:
        git_lab_discussion: GitLabDiscussion = GitLabDiscussion.objects.get_or_create(id=discussion_dict.get("id"))[0]
        git_lab_discussion.individual_note = discussion_dict.get("individual_note")
        notes: list[GitLabNoteTypedDict] | None = discussion_dict.get("notes")
        if notes is not None:
            for note in notes:
                git_lab_note: GitLabNote = GitLabNote.objects.get_or_create(id=note.get("id"))[0]
                git_lab_note.body = note.get("body")
                git_lab_note.created_at = convert_and_enforce_utc_timezone(datetime_string=note.get("created_at"))
                git_lab_note.discussion = git_lab_discussion
                git_lab_note.noteable_id = note.get("noteable_id")
                git_lab_note.noteable_iid = note.get("noteable_iid")
                git_lab_note.noteable_type = note.get("noteable_type")
                project: GitLabProject | None = GitLabProject.objects.filter(id=note.get("project_id")).first()
                if project is not None:
                    git_lab_note.project = project
                    git_lab_discussion.project = project
                git_lab_note.save()
                git_lab_note.system = note.get("system")
                git_lab_note.type = note.get("type")
                git_lab_note.updated_at = convert_and_enforce_utc_timezone(datetime_string=note.get("updated_at"))
        git_lab_discussion.save()
    return JsonResponse(data=all_discussion_dicts, safe=False)
