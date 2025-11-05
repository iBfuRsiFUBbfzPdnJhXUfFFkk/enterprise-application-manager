from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncMilestone


def gitlab_sync_milestones_view(request: HttpRequest) -> HttpResponse:
    """
    GitLab Milestones list view with search and filtering.
    """
    search_query = request.GET.get("search", "").strip()

    milestones = GitLabSyncMilestone.objects.all().select_related("project", "group").order_by("-due_date", "-created_at")

    if search_query:
        milestones = milestones.filter(title__icontains=search_query) | milestones.filter(
            description__icontains=search_query
        ) | milestones.filter(project__path_with_namespace__icontains=search_query)

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/milestones.html",
        context={
            "milestones": milestones,
            "total_count": milestones.count(),
            "search_query": search_query,
        },
    )
