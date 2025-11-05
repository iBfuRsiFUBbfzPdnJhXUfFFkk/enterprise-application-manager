from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.application.application_add_view import application_add_view
from core.views.application.application_delete_view import application_delete_view
from core.views.application.application_detail_view import application_detail_view
from core.views.application.application_edit_view import application_edit_view
from core.views.application.application_logging_dashboard_view import (
    application_logging_dashboard_view,
)
from core.views.application.application_pipeline_dashboard_view import (
    application_pipeline_dashboard_view,
)
from core.views.application.application_view import application_view

urlpatterns_application: list[URLPattern | URLResolver] = [
    *create_generic_urlpatterns(
        name="application",
        view=application_view,
        view_edit=application_edit_view,
        view_new=application_add_view,
    ),
    path(name="application_detail", route="application/<int:model_id>/", view=application_detail_view),
    path(name="application_delete", route="application/delete/<int:model_id>/", view=application_delete_view),
    path(
        name="application_pipeline_dashboard",
        route="application/pipeline-dashboard/",
        view=application_pipeline_dashboard_view,
    ),
    path(
        name="application_logging_dashboard",
        route="application/logging-dashboard/",
        view=application_logging_dashboard_view,
    ),
]
