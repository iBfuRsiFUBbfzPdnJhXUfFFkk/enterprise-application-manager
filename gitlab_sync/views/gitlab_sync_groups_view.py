from django.db.models import Count
from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncGroup


def gitlab_sync_groups_view(request: HttpRequest) -> HttpResponse:
    """
    GitLab Groups list view with search and filtering.
    """
    search_query = request.GET.get("search", "").strip()
    visibility_filter = request.GET.get("visibility", "").strip()

    groups = GitLabSyncGroup.objects.all().annotate(
        projects_count=Count("projects"),
        issues_count=Count("issues"),
        merge_requests_count=Count("merge_requests"),
    ).order_by("-last_synced_at")

    if search_query:
        groups = groups.filter(full_name__icontains=search_query) | groups.filter(
            full_path__icontains=search_query
        )

    if visibility_filter:
        groups = groups.filter(visibility=visibility_filter)

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/groups.html",
        context={
            "groups": groups,
            "total_count": groups.count(),
            "search_query": search_query,
            "visibility_filter": visibility_filter,
        },
    )
