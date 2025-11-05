from django.db.models import Count
from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncEpic


def gitlab_sync_epics_view(request: HttpRequest) -> HttpResponse:
    """
    GitLab Epics list view with search and filtering.
    """
    search_query = request.GET.get("search", "").strip()
    state_filter = request.GET.get("state", "").strip()

    epics = GitLabSyncEpic.objects.all().select_related("group", "author", "parent_epic").annotate(
        issues_count=Count("issues"),
        child_epics_count=Count("child_epics"),
    ).order_by("-updated_at")

    if search_query:
        epics = epics.filter(title__icontains=search_query)

    if state_filter:
        epics = epics.filter(state=state_filter)

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/epics.html",
        context={
            "epics": epics,
            "total_count": epics.count(),
            "search_query": search_query,
            "state_filter": state_filter,
        },
    )
