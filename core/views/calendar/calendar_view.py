from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render


def calendar_view(request: HttpRequest) -> HttpResponse:
    """Render the main calendar interface."""
    return base_render(
        request=request,
        template_name='authenticated/calendar/calendar.html',
        context={},
    )
