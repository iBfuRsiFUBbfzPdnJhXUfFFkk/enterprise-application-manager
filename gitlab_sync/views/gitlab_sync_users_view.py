from django.db.models import Count
from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncUser


def gitlab_sync_users_view(request: HttpRequest) -> HttpResponse:
    """
    GitLab Users list view with search and filtering.
    """
    search_query = request.GET.get("search", "").strip()
    state_filter = request.GET.get("state", "").strip()

    users = GitLabSyncUser.objects.all().annotate(
        commits_count=Count("commits_authored"),
        issues_count=Count("issues_authored"),
        merge_requests_count=Count("merge_requests_authored"),
    ).order_by("-last_synced_at")

    if search_query:
        users = users.filter(name__icontains=search_query) | users.filter(
            username__icontains=search_query
        ) | users.filter(email__icontains=search_query)

    if state_filter:
        users = users.filter(state=state_filter)

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/users.html",
        context={
            "users": users,
            "total_count": users.count(),
            "search_query": search_query,
            "state_filter": state_filter,
        },
    )
