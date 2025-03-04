from collections import defaultdict
from datetime import date, timedelta
from time import time

from django.http import HttpRequest, HttpResponse

from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint
from core.models.person import Person
from core.models.secret import Secret
from core.models.sprint import Sprint
from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500
from core.views.this_api.this_api_update_code_reviews.fetch_and_filter_pull_requests import \
    fetch_and_filter_pull_requests
from core.views.this_api.this_api_update_code_reviews.fetch_approvals_for_pull_requests import \
    fetch_approvals_for_pull_requests, MergeRequest
from core.views.this_api.this_api_update_code_reviews.fetch_discussions_for_pull_requests import \
    fetch_discussions_for_pull_requests, NoteEntry
from core.views.this_api.this_api_update_code_reviews.process_discussions import process_discussions


def this_api_update_code_reviews_view(request: HttpRequest) -> HttpResponse:
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
    current_date: date = date.today()
    try:
        sprints = Sprint.objects.filter(
            date_start__lte=current_date,
            date_end__gte=(current_date - timedelta(days=3)),
        )
        if not sprints.exists():
            return generic_500(request=request)
    except Sprint.DoesNotExist:
        return generic_500(request=request)
    for sprint in sprints:
        closed_after: str = sprint.date_start.strftime("%Y-%m-%dT%H:%M:%SZ")
        closed_before: str = sprint.date_end.strftime("%Y-%m-%dT%H:%M:%SZ")

        pull_requests = fetch_and_filter_pull_requests(
            closed_after=closed_after,
            closed_before=closed_before,
            connection_gitlab_hostname=connection_gitlab_hostname,
            connection_gitlab_api_version=connection_gitlab_api_version,
            connection_gitlab_group_id=connection_gitlab_group_id,
            decrypted_token=decrypted_token,
        )
        if not pull_requests:
            continue
        metrics = defaultdict(lambda: {"approvals": 0, "comments": 0, "threads": 0})

        for pull_request in pull_requests:
            project_id = pull_request["project_id"]
            pull_request_iid = pull_request["iid"]

            approvals: MergeRequest | None = fetch_approvals_for_pull_requests(
                connection_gitlab_hostname=connection_gitlab_hostname,
                connection_gitlab_api_version=connection_gitlab_api_version,
                decrypted_token=decrypted_token,
                project_id=str(project_id),
                pull_request_iid=str(pull_request_iid),
            )
            if not approvals:
                continue
            approvals_mod = [a.get("user", {}).get("username", "") for a in approvals.get("approved_by", [])]
            approvals_mod = [a for a in approvals_mod if a]
            for approval_m in approvals_mod:
                metrics[approval_m]["approvals"] += 1
            discussions: list[NoteEntry] | None = fetch_discussions_for_pull_requests(
                connection_gitlab_hostname=connection_gitlab_hostname,
                connection_gitlab_api_version=connection_gitlab_api_version,
                decrypted_token=decrypted_token,
                project_id=str(project_id),
                pull_request_iid=str(pull_request_iid),
            )
            if not discussions:
                continue
            comments, threads = process_discussions(discussions, approvals_mod)
            for approval_m in approvals_mod:
                metrics[approval_m]["comments"] += comments
                metrics[approval_m]["threads"] += threads
        updated_count = 0
        for username, counts in metrics.items():
            try:
                user = Person.objects.get(gitlab_sync_username=username)
                KeyPerformanceIndicatorSprint.objects.update_or_create(
                    person_developer=user,
                    sprint=sprint,
                    defaults={
                        "number_of_code_reviews_submitted": counts["approvals"],
                        "number_of_comments_made": counts["comments"],
                        "number_of_threads_resolved": counts["threads"],
                    }
                )
                updated_count += 1
            except Person.DoesNotExist:
                continue
    end_time: float = time()
    execution_time_in_seconds: float = end_time - start_time
    return base_render(
        context={
            "execution_time_in_seconds": execution_time_in_seconds,
            "payload": {
            },
        },
        request=request,
        template_name="authenticated/action/action_success.html"
    )
