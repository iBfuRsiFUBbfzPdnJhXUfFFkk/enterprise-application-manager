from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncIssue


def gitlab_sync_issues_view(request: HttpRequest) -> HttpResponse:
    """
    GitLab Issues list view with search and filtering.
    """
    search_query = request.GET.get("search", "").strip()
    state_filter = request.GET.get("state", "").strip()
    issue_type_filter = request.GET.get("issue_type", "").strip()

    issues = GitLabSyncIssue.objects.all().select_related("project", "author", "epic").prefetch_related(
        "assignees"
    ).order_by("-updated_at")

    if search_query:
        issues = issues.filter(title__icontains=search_query)

    if state_filter:
        issues = issues.filter(state=state_filter)

    if issue_type_filter:
        issues = issues.filter(issue_type=issue_type_filter)

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/issues.html",
        context={
            "issues": issues,
            "total_count": issues.count(),
            "search_query": search_query,
            "state_filter": state_filter,
            "issue_type_filter": issue_type_filter,
        },
    )
