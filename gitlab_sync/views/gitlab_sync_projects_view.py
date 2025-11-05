from django.db.models import Count
from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncProject


def gitlab_sync_projects_view(request: HttpRequest) -> HttpResponse:
    """
    GitLab Projects list view with search and filtering.
    """
    search_query = request.GET.get("search", "").strip()
    visibility_filter = request.GET.get("visibility", "").strip()
    archived_filter = request.GET.get("archived", "").strip()

    projects = GitLabSyncProject.objects.all().select_related("group", "application").annotate(
        issues_count=Count("issues"),
        merge_requests_count=Count("merge_requests"),
        pipelines_count=Count("pipelines"),
    ).order_by("-last_activity_at")

    if search_query:
        projects = projects.filter(name__icontains=search_query) | projects.filter(
            path_with_namespace__icontains=search_query
        )

    if visibility_filter:
        projects = projects.filter(visibility=visibility_filter)

    if archived_filter == "true":
        projects = projects.filter(archived=True)
    elif archived_filter == "false":
        projects = projects.filter(archived=False)

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/projects.html",
        context={
            "projects": projects,
            "total_count": projects.count(),
            "search_query": search_query,
            "visibility_filter": visibility_filter,
            "archived_filter": archived_filter,
        },
    )
