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
from core.views.this_api.this_api_update_issues_authored_view.fetch_issues_authored import fetch_issues_authored


def this_api_update_issues_authored_view(request: HttpRequest) -> HttpResponse:
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
        closed_after: str = sprint.date_start.isoformat()
        closed_before: str = sprint.date_end.isoformat()

        author_counts = fetch_issues_authored(
            connection_gitlab_hostname=connection_gitlab_hostname,
            connection_gitlab_api_version=connection_gitlab_api_version,
            connection_gitlab_group_id=connection_gitlab_group_id,
            decrypted_token=decrypted_token,
            closed_after=closed_after,
            closed_before=closed_before,
        )
        if not author_counts:
            continue
        updated_count = 0
        for gitlab_username, issue_count in author_counts.items():
            try:
                developer = Person.objects.get(gitlab_sync_username=gitlab_username)
                kpi, created = KeyPerformanceIndicatorSprint.objects.update_or_create(
                    person_developer=developer,
                    sprint=sprint,
                )
                kpi.number_of_issues_written = issue_count
                kpi.save()
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
