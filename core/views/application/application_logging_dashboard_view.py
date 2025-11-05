from django.db.models import Q
from django.http import HttpRequest, HttpResponse

from core.models.application import Application
from core.models.common.enums.centralized_logging_status_choices import (
    CENTRALIZED_LOGGING_STATUS_IMPLEMENTED,
    CENTRALIZED_LOGGING_STATUS_NOT_IMPLEMENTED,
    CENTRALIZED_LOGGING_STATUS_UNKNOWN,
)
from core.utilities.base_render import base_render


def application_logging_dashboard_view(request: HttpRequest) -> HttpResponse:
    applications = Application.objects.all()

    implemented_apps = applications.filter(
        centralized_logging_status=CENTRALIZED_LOGGING_STATUS_IMPLEMENTED
    )
    not_implemented_apps = applications.filter(
        centralized_logging_status=CENTRALIZED_LOGGING_STATUS_NOT_IMPLEMENTED
    )
    unknown_apps = applications.filter(
        Q(centralized_logging_status=CENTRALIZED_LOGGING_STATUS_UNKNOWN)
        | Q(centralized_logging_status__isnull=True)
    )

    total_count = applications.count()
    implemented_count = implemented_apps.count()
    not_implemented_count = not_implemented_apps.count()
    unknown_count = unknown_apps.count()

    implemented_percentage = (
        (implemented_count / total_count * 100) if total_count > 0 else 0
    )
    not_implemented_percentage = (
        (not_implemented_count / total_count * 100) if total_count > 0 else 0
    )
    unknown_percentage = (unknown_count / total_count * 100) if total_count > 0 else 0

    context = {
        "total_count": total_count,
        "implemented_count": implemented_count,
        "not_implemented_count": not_implemented_count,
        "unknown_count": unknown_count,
        "implemented_percentage": round(implemented_percentage, 1),
        "not_implemented_percentage": round(not_implemented_percentage, 1),
        "unknown_percentage": round(unknown_percentage, 1),
        "implemented_apps": implemented_apps,
        "not_implemented_apps": not_implemented_apps,
        "unknown_apps": unknown_apps,
    }

    return base_render(
        context=context,
        request=request,
        template_name="authenticated/application/application_logging_dashboard.html",
    )
