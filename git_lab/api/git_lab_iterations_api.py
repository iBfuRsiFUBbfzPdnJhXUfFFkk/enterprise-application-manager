from typing import cast

from django.db.models import QuerySet
from django.http import HttpRequest, JsonResponse, HttpResponse
from gitlab import Gitlab
from gitlab.v4.objects import GroupIteration, Group

from core.utilities.cast_query_set import cast_query_set
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.models.git_lab_group import GitLabGroup


def git_lab_iterations_api(
        request: HttpRequest,
) -> JsonResponse | HttpResponse:
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
            val=group.iterations.list(all=True)
        )
        for iteration in iterations:
            all_iterations.add(iteration)
    iteration_dicts: list[dict] = [iteration.asdict() for iteration in list(all_iterations)]
    return JsonResponse(data=iteration_dicts, safe=False)
