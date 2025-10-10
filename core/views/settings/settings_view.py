from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render


@login_required
def settings_view(request: HttpRequest) -> HttpResponse:
    """
    Display the settings page where users can manage their preferences
    and application data stored in localStorage.
    """
    return base_render(
        context={},
        request=request,
        template_name='authenticated/settings.html',
    )
