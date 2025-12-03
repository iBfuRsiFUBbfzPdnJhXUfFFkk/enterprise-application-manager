from django.http import HttpRequest, HttpResponse

from core.models.application import Application
from core.models.application_pin import ApplicationPin
from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.base_render import base_render
from core.utilities.get_user_from_request import get_user_from_request


def application_view(request: HttpRequest) -> HttpResponse:
    user = get_user_from_request(request=request)

    # Get all applications
    all_applications = Application.objects.all()

    # Get user's pinned application IDs and their order
    pinned_apps_data = {}
    if user:
        pins = ApplicationPin.objects.filter(user=user).select_related('application')
        pinned_apps_data = {
            pin.application.id: pin.order
            for pin in pins
        }
        pinned_app_ids = set(pinned_apps_data.keys())

        # Separate pinned and unpinned applications
        pinned_applications = [
            app for app in all_applications
            if app.id in pinned_app_ids
        ]
        unpinned_applications = [
            app for app in all_applications
            if app.id not in pinned_app_ids
        ]

        # Sort pinned applications by order
        pinned_applications.sort(key=lambda app: pinned_apps_data[app.id])
    else:
        pinned_applications = []
        unpinned_applications = list(all_applications)

    context = {
        'hostname_gitlab': ThisServerConfiguration.current().connection_git_lab_hostname,
        'models': all_applications,  # Keep for backward compatibility
        'pinned_applications': pinned_applications,
        'unpinned_applications': unpinned_applications,
        'pinned_app_ids': list(pinned_apps_data.keys()) if user else [],
    }

    return base_render(
        context=context,
        request=request,
        template_name="authenticated/application/application.html"
    )
