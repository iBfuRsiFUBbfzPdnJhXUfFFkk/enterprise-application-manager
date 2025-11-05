from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncEvent


def gitlab_sync_event_detail_view(request: HttpRequest, event_id: int) -> HttpResponse:
    """Display detail view for a specific GitLab event."""
    event = get_object_or_404(
        GitLabSyncEvent.objects.select_related("project", "author"),
        id=event_id
    )

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/event_detail.html",
        context={
            "event": event,
        },
    )
