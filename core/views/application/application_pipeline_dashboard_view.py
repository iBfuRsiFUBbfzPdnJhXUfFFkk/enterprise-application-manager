from django.db.models import Count, Q
from django.http import HttpRequest, HttpResponse

from core.models.application import Application
from core.models.common.enums.pipeline_status_choices import (
    PIPELINE_STATUS_FAILING,
    PIPELINE_STATUS_PASSING,
    PIPELINE_STATUS_UNKNOWN,
)
from core.utilities.base_render import base_render


def application_pipeline_dashboard_view(request: HttpRequest) -> HttpResponse:
    applications = Application.objects.all()

    passing_apps = applications.filter(pipeline_status=PIPELINE_STATUS_PASSING)
    failing_apps = applications.filter(pipeline_status=PIPELINE_STATUS_FAILING)
    unknown_apps = applications.filter(
        Q(pipeline_status=PIPELINE_STATUS_UNKNOWN) | Q(pipeline_status__isnull=True)
    )

    total_count = applications.count()
    passing_count = passing_apps.count()
    failing_count = failing_apps.count()
    unknown_count = unknown_apps.count()

    passing_percentage = (passing_count / total_count * 100) if total_count > 0 else 0
    failing_percentage = (failing_count / total_count * 100) if total_count > 0 else 0
    unknown_percentage = (unknown_count / total_count * 100) if total_count > 0 else 0

    context = {
        "total_count": total_count,
        "passing_count": passing_count,
        "failing_count": failing_count,
        "unknown_count": unknown_count,
        "passing_percentage": round(passing_percentage, 1),
        "failing_percentage": round(failing_percentage, 1),
        "unknown_percentage": round(unknown_percentage, 1),
        "passing_apps": passing_apps,
        "failing_apps": failing_apps,
        "unknown_apps": unknown_apps,
    }

    return base_render(
        context=context,
        request=request,
        template_name="authenticated/application/application_pipeline_dashboard.html",
    )
