from re import match
from time import time
from typing import TypedDict, Literal

from django.http import HttpRequest, HttpResponse
from gitlab import Gitlab
from gitlab.base import RESTObject
from gitlab.v4.objects import GroupMergeRequest, ProjectMergeRequestApproval

from core.models.person import Person
from core.models.sprint import Sprint
from core.utilities.base_render import base_render
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.utilities.git_lab.get_git_lab_group_id import get_git_lab_group_id
from core.views.generic.generic_500 import generic_500
from core.views.this_api.this_api_sync_git_lab_view.common.fetch_group_merge_requests import fetch_group_merge_requests
from core.views.this_api.this_api_sync_git_lab_view.common.fetch_issues_by_iterations import fetch_issues_by_iterations
from core.views.this_api.this_api_sync_git_lab_view.common.fetch_project_merge_requests_approvals import \
    fetch_project_merge_requests_approvals
from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint


class IssueMap(TypedDict):
    number_of_issues_authored: int
    number_of_issues_committed_to: int
    number_of_issues_delivered_on: int
    number_of_issues_weights_committed_to: int
    number_of_issues_weights_delivered_on: int
    project_ids_worked_on: list[str]


def create_initial_issue_map() -> IssueMap:
    return {
        "number_of_issues_authored": 0,
        "number_of_issues_committed_to": 0,
        "number_of_issues_delivered_on": 0,
        "number_of_issues_weights_committed_to": 0,
        "number_of_issues_weights_delivered_on": 0,
        "project_ids_worked_on": [],
    }


def this_api_sync_git_lab_view(request: HttpRequest) -> HttpResponse:
    start_time: float = time()
    git_lab_client: Gitlab | None = get_git_lab_client()
    git_lab_group_id: str | None = get_git_lab_group_id()
    if git_lab_client is None or git_lab_group_id is None:
        return generic_500(request=request)
    current_sprint: Sprint | None = Sprint.current_sprint()
    issues_map: dict[str, IssueMap] = {}
    if current_sprint is not None:
        all_group_issues: list[RESTObject] = fetch_issues_by_iterations(
            iteration_ids=current_sprint.iteration_ids
        ) or []
        all_group_merge_requests: list[GroupMergeRequest] = fetch_group_merge_requests() or []
        for group_merge_request in all_group_merge_requests:
            if group_merge_request.state == "merged":
                all_approvals: list[ProjectMergeRequestApproval] | None = fetch_project_merge_requests_approvals(
                    merge_request_internal_identification_iid=group_merge_request.iid,
                    project_id=group_merge_request.project_id,
                )
                print(all_approvals)
        for group_issue in all_group_issues:
            project_id: int | None = group_issue.project_id
            state: str | None = group_issue.state
            weight: int = group_issue.weight or 0
            author: dict[Literal["username"], str] = group_issue.author
            author_username: str | None = author["username"]
            if author_username is not None:
                if author_username not in issues_map:
                    issues_map[author_username] = create_initial_issue_map()
                issues_map[author_username]["number_of_issues_authored"] += 1
            assignees: list[dict[Literal["username"], str]] = group_issue.assignees or []
            for assignee in assignees:
                assignee_username: str | None = assignee["username"]
                if assignee_username is None:
                    continue
                if assignee_username not in issues_map:
                    issues_map[assignee_username] = create_initial_issue_map()
                issues_map[assignee_username]["number_of_issues_committed_to"] += 1
                issues_map[assignee_username]["number_of_issues_weights_committed_to"] += weight
                if state == "closed":
                    issues_map[assignee_username]["number_of_issues_delivered_on"] += 1
                    issues_map[assignee_username]["number_of_issues_weights_delivered_on"] += weight
                    issues_map[assignee_username]["project_ids_worked_on"].append(str(project_id))
    number_of_new_kpi_records_created: int = 0
    number_of_updated_kpi_records: int = 0
    for git_lab_username, issue_map in issues_map.items():
        if match(r'^(project|group).*bot.*$', git_lab_username):
            continue
        person_instance: Person | None = Person.objects.filter(gitlab_sync_username=git_lab_username).first()
        if person_instance is None:
            continue
        kpi_instance, did_create = KeyPerformanceIndicatorSprint.objects.get_or_create(
            person_developer=person_instance,
            sprint=current_sprint,
        )
        kpi_instance.number_of_context_switches = len(issue_map["project_ids_worked_on"])
        kpi_instance.number_of_issues_written = issue_map["number_of_issues_authored"]
        kpi_instance.number_of_story_points_committed_to = issue_map["number_of_issues_weights_committed_to"]
        kpi_instance.number_of_story_points_delivered = issue_map["number_of_issues_weights_delivered_on"]
        kpi_instance.save()
        if did_create:
            number_of_new_kpi_records_created += 1
        else:
            number_of_updated_kpi_records += 1
    end_time: float = time()
    execution_time_in_seconds: float = end_time - start_time
    return base_render(
        context={
            "execution_time_in_seconds": execution_time_in_seconds,
            "payload": {
                "number_of_new_kpi_records_created": number_of_new_kpi_records_created,
                "number_of_updated_kpi_records": number_of_updated_kpi_records,
            },
        },
        request=request,
        template_name="authenticated/action/action_success.html"
    )
