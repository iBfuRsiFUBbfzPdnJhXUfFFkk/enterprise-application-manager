from collections import defaultdict
from datetime import date, timedelta
from time import time

from django.http import HttpRequest, HttpResponse

from core.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint
from core.models.person import Person
from core.models.secret import Secret
from core.models.sprint import Sprint
from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500
from core.views.this_api.this_api_update_code_churn_view.fetch_merged_pull_requests import fetch_merged_pull_requests
from core.views.this_api.this_api_update_code_churn_view.fetch_pull_request_changes import fetch_pull_request_changes, \
    FetchPullRequestChangesReturn
from core.views.this_api.this_api_update_code_churn_view.update_code_churn_typed_dicts import MergeRequest, User


def this_api_update_code_churn_view(request: HttpRequest) -> HttpResponse:
    start_time: float = time()
    this_server_configuration: ThisServerConfiguration | None = ThisServerConfiguration.objects.last()
    if this_server_configuration is None:
        return generic_500(request=request)
    connection_gitlab_hostname: str | None = this_server_configuration.connection_gitlab_hostname
    if connection_gitlab_hostname is None:
        return generic_500(request=request)
    connection_gitlab_api_version: str | None = this_server_configuration.connection_gitlab_api_version
    if connection_gitlab_api_version is None:
        return generic_500(request=request)
    connection_gitlab_group_id: str | None = this_server_configuration.connection_gitlab_group_id
    if connection_gitlab_group_id is None:
        return generic_500(request=request)
    connection_gitlab_token_secret: Secret | None = this_server_configuration.connection_gitlab_token
    if connection_gitlab_token_secret is None:
        return generic_500(request=request)
    decrypted_token: str | None = connection_gitlab_token_secret.get_encrypted_value()
    if decrypted_token is None:
        return generic_500(request=request)
    number_of_key_performance_indicator_sprints_updated: int = 0
    current_date: date = date.today()
    try:
        sprints = Sprint.objects.filter(
            date_end__gte=(current_date - timedelta(days=3)),
            date_start__lte=current_date,
        )
        if not sprints.exists():
            return generic_500(request=request)
    except Sprint.DoesNotExist:
        return generic_500(request=request)
    for sprint in sprints:
        merged_after: str = sprint.date_start.isoformat()
        merged_before: str = sprint.date_end.isoformat()
        pull_requests: list[MergeRequest] | None = fetch_merged_pull_requests(
            connection_gitlab_hostname=connection_gitlab_hostname,
            connection_gitlab_api_version=connection_gitlab_api_version,
            connection_gitlab_group_id=connection_gitlab_group_id,
            decrypted_token=decrypted_token,
            merged_after=merged_after,
            merged_before=merged_before,
        )
        if pull_requests is None:
            continue
        lines_data = defaultdict(lambda: {"added": 0, "removed": 0})
        for pull_request in pull_requests:
            try:
                project_id: int | None = pull_request["project_id"]
                if project_id is None:
                    continue
                iid: int | None = pull_request["iid"]
                if iid is None:
                    continue
                author: User | None = pull_request["author"]
                if author is None:
                    continue
                username: str | None = author["username"]
                if username is None:
                    continue
                changes: FetchPullRequestChangesReturn | None = fetch_pull_request_changes(
                    connection_gitlab_hostname=connection_gitlab_hostname,
                    connection_gitlab_api_version=connection_gitlab_api_version,
                    connection_gitlab_group_id=connection_gitlab_group_id,
                    decrypted_token=decrypted_token,
                    project_id=str(project_id),
                    pull_request_iid=str(iid)
                )
                if changes is None:
                    continue
                lines_data[username]["added"] += changes["added"]
                lines_data[username]["removed"] += changes["removed"]
            except KeyError:
                continue
        for username, stats in lines_data.items():
            try:
                person: Person | None = Person.objects.get(gitlab_sync_username=username)
                if person is None:
                    continue
                key_performance_indicator_sprint, created = KeyPerformanceIndicatorSprint.objects.get_or_create(
                    person_developer=person,
                    sprint=sprint,
                )
                key_performance_indicator_sprint.number_of_code_lines_added = stats["added"]
                key_performance_indicator_sprint.number_of_code_lines_removed = stats["removed"]
                key_performance_indicator_sprint.save()
                number_of_key_performance_indicator_sprints_updated += 1
            except Person.DoesNotExist:
                continue
    end_time: float = time()
    execution_time_in_seconds: float = end_time - start_time
    return base_render(
        context={
            "execution_time_in_seconds": execution_time_in_seconds,
            "number_of_key_performance_indicator_sprints_updated": number_of_key_performance_indicator_sprints_updated,
        },
        request=request,
        template_name="authenticated/action/action_success.html"
    )
