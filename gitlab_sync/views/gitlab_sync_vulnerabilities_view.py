from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncVulnerability


def gitlab_sync_vulnerabilities_view(request: HttpRequest) -> HttpResponse:
    """
    GitLab Vulnerabilities list view with search and filtering.
    """
    search_query = request.GET.get("search", "").strip()
    severity_filter = request.GET.get("severity", "").strip()
    state_filter = request.GET.get("state", "").strip()

    vulnerabilities = GitLabSyncVulnerability.objects.all().select_related(
        "project", "author", "resolved_by"
    ).order_by("-detected_at")

    if search_query:
        vulnerabilities = vulnerabilities.filter(title__icontains=search_query)

    if severity_filter:
        vulnerabilities = vulnerabilities.filter(severity=severity_filter)

    if state_filter:
        vulnerabilities = vulnerabilities.filter(state=state_filter)

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/vulnerabilities.html",
        context={
            "vulnerabilities": vulnerabilities,
            "total_count": vulnerabilities.count(),
            "search_query": search_query,
            "severity_filter": severity_filter,
            "state_filter": state_filter,
        },
    )
