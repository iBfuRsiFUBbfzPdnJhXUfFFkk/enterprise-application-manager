from typing import cast

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab
from gitlab.v4.objects import GroupMember, Group

from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import convert_and_enforce_utc_timezone
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.models.common.typed_dicts.git_lab_user_typed_dict import GitLabUserTypedDict
from git_lab.models.git_lab_group import GitLabGroup
from git_lab.models.git_lab_iteration import GitLabIteration
from git_lab.models.git_lab_user import GitLabUser


def get_iteration_key(iteration: GitLabIteration) -> str:
    return f"{iteration.start_date}=>{iteration.due_date}"

def scrum_sprints_api(
        request: HttpRequest,
) -> JsonResponse | HttpResponse:
    git_lab_iterations: QuerySet[GitLabIteration] = cast_query_set(
        typ=GitLabIteration,
        val=GitLabIteration.objects.all(),
    )
    iteration_groupings: dict[str, set[GitLabIteration]] = {}
    for git_lab_iteration in git_lab_iterations:
        key: str = get_iteration_key(iteration=git_lab_iteration)
        if key not in iteration_groupings:
            iteration_groupings[key] = set()
        iteration_groupings[key].add(git_lab_iteration)
    return JsonResponse(data=iteration_groupings, safe=False)
