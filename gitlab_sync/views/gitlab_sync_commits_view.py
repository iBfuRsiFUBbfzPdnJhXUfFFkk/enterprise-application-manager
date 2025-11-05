from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncCommit


def gitlab_sync_commits_view(request: HttpRequest) -> HttpResponse:
    """
    GitLab Commits list view with search and filtering.
    """
    search_query = request.GET.get("search", "").strip()

    commits = GitLabSyncCommit.objects.all().select_related("project", "repository", "author").order_by("-committed_date")

    if search_query:
        commits = commits.filter(title__icontains=search_query) | commits.filter(
            sha__icontains=search_query
        ) | commits.filter(author_name__icontains=search_query)

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/commits.html",
        context={
            "commits": commits,
            "total_count": commits.count(),
            "search_query": search_query,
        },
    )
