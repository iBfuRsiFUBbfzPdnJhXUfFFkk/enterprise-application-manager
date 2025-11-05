from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncBranch


def gitlab_sync_branches_view(request: HttpRequest) -> HttpResponse:
    """
    GitLab Branches list view with search and filtering.
    """
    search_query = request.GET.get("search", "").strip()

    branches = GitLabSyncBranch.objects.all().select_related("project", "repository").order_by("-default", "name")

    if search_query:
        branches = branches.filter(name__icontains=search_query) | branches.filter(
            project__path_with_namespace__icontains=search_query
        ) | branches.filter(commit_title__icontains=search_query)

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/branches.html",
        context={
            "branches": branches,
            "total_count": branches.count(),
            "search_query": search_query,
        },
    )
