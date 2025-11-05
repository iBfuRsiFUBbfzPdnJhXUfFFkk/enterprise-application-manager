from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncEvent


def gitlab_sync_events_view(request: HttpRequest) -> HttpResponse:
    """Display list of GitLab events with search."""
    search_query = request.GET.get("search", "").strip()

    events = GitLabSyncEvent.objects.all().select_related("project", "author")

    if search_query:
        events = events.filter(
            action_name__icontains=search_query
        ) | events.filter(
            target_title__icontains=search_query
        ) | events.filter(
            target_type__icontains=search_query
        ) | events.filter(
            project__name__icontains=search_query
        ) | events.filter(
            author__name__icontains=search_query
        )

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/events.html",
        context={
            "events": events[:500],  # Limit to 500 events
            "search_query": search_query,
            "total_count": events.count(),
        },
    )
