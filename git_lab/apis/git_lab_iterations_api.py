from typing import cast

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab
from gitlab.v4.objects import GroupIteration, Group

from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import convert_and_enforce_utc_timezone
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.apis.common.get_common_query_parameters import GitLabApiCommonQueryParameters, get_common_query_parameters
from git_lab.models.common.typed_dicts.git_lab_iteration_typed_dict import GitLabIterationTypedDict
from git_lab.models.git_lab_group import GitLabGroup
from git_lab.models.git_lab_iteration import GitLabIteration
from scrum.models.scrum_sprint import ScrumSprint


def git_lab_iterations_api(
        request: HttpRequest,
) -> JsonResponse | HttpResponse:
    query_parameters: GitLabApiCommonQueryParameters = get_common_query_parameters(request=request)
    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        return generic_500(request=request)
    git_lab_groups: QuerySet[GitLabGroup] = cast_query_set(
        typ=GitLabGroup,
        val=GitLabGroup.objects.all(),
    )
    all_iterations: set[GroupIteration] = set()
    for git_lab_group in git_lab_groups:
        group: Group | None = git_lab_client.groups.get(id=git_lab_group.id)
        if group is None:
            continue
        iterations: list[GroupIteration] = cast(
            typ=list[GroupIteration],
            val=group.iterations.list(**query_parameters)
        )
        all_iterations.update(iterations)
    iteration_dicts: list[GitLabIterationTypedDict] = [iteration.asdict() for iteration in list(all_iterations)]
    for iteration_dict in iteration_dicts:
        iteration_id: int | None = iteration_dict.get("id")
        if iteration_id is None:
            continue
        get_or_create_tuple: tuple[GitLabIteration, bool] = GitLabIteration.objects.get_or_create(id=iteration_id)
        git_lab_iteration: GitLabIteration = get_or_create_tuple[0]
        git_lab_iteration.description = iteration_dict.get("description")
        git_lab_iteration.due_date = iteration_dict.get("due_date")
        git_lab_iteration.iid = iteration_dict.get("iid")
        git_lab_iteration.sequence = iteration_dict.get("sequence")
        git_lab_iteration.start_date = iteration_dict.get("start_date")
        git_lab_iteration.state = iteration_dict.get("state")
        git_lab_iteration.title = iteration_dict.get("title") or f"No Title: {iteration_dict.get("due_date")}"
        git_lab_iteration.web_url = iteration_dict.get("web_url")
        git_lab_iteration.created_at = convert_and_enforce_utc_timezone(
            datetime_string=iteration_dict.get("created_at")
        )
        git_lab_iteration.updated_at = convert_and_enforce_utc_timezone(
            datetime_string=iteration_dict.get("updated_at")
        )
        git_lab_iteration.group = GitLabGroup.objects.filter(id=iteration_dict.get("group_id")).first()
        if git_lab_iteration.due_date is not None:
            scrum_sprint: ScrumSprint | None = ScrumSprint.objects.filter(
                date_end=git_lab_iteration.due_date,
            ).first()
            if scrum_sprint is not None:
                git_lab_iteration.scrum_sprint = scrum_sprint
        git_lab_iteration.save()
    return JsonResponse(data=iteration_dicts, safe=False)
