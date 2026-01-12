from django.urls import URLPattern, URLResolver, path

from core.views.application.application_add_view import application_add_view
from core.views.application.application_delete_view import application_delete_view
from core.views.application.application_detail_view import application_detail_view
from core.views.application.application_edit_view import application_edit_view
from core.views.application.application_export_contacts_docx_view import (
    application_export_contacts_docx_view,
)
from core.views.application.application_export_docx_view import application_export_docx_view
from core.views.application.application_logging_dashboard_view import (
    application_logging_dashboard_view,
)
from core.views.application.application_pin_reorder_view import application_pin_reorder_view
from core.views.application.application_pin_toggle_view import application_pin_toggle_view
from core.views.application.application_pipeline_dashboard_view import (
    application_pipeline_dashboard_view,
)
from core.views.application.application_procedure_add_view import application_procedure_add_view
from core.views.application.application_procedure_delete_view import application_procedure_delete_view
from core.views.application.application_procedure_edit_view import application_procedure_edit_view
from core.views.application.application_procedure_list_view import application_procedure_list_view
from core.views.application.application_procedure_reorder_view import application_procedure_reorder_view
from core.views.application.application_view import application_view

urlpatterns_application: list[URLPattern | URLResolver] = [
    path("application/", application_view, name="application"),
    path("application/edit/<int:model_id>/", application_edit_view, name="application_edit"),
    path("application/new/", application_add_view, name="application_new"),
    path("application/<int:model_id>/", application_detail_view, name="application_detail"),
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
    # Procedure management URLs
    path(
        name="application_procedure_list",
        route="application/<int:model_id>/procedure/",
        view=application_procedure_list_view,
    ),
    path(
        name="application_procedure_add",
        route="application/<int:model_id>/procedure/add/",
        view=application_procedure_add_view,
    ),
    path(
        name="application_procedure_edit",
        route="application/<int:model_id>/procedure/<int:step_id>/edit/",
        view=application_procedure_edit_view,
    ),
    path(
        name="application_procedure_delete",
        route="application/<int:model_id>/procedure/<int:step_id>/delete/",
        view=application_procedure_delete_view,
    ),
    path(
        name="application_procedure_reorder",
        route="application/<int:model_id>/procedure/reorder/",
        view=application_procedure_reorder_view,
    ),
    # Pin management URLs
    path(
        name="application_pin_toggle",
        route="application/pin/toggle/",
        view=application_pin_toggle_view,
    ),
    path(
        name="application_pin_reorder",
        route="application/pin/reorder/",
        view=application_pin_reorder_view,
    ),
    # Export
    path(
        name="application_export_docx",
        route="application/export/",
        view=application_export_docx_view,
    ),
    path(
        name="application_export_contacts_docx",
        route="application/export-contacts/",
        view=application_export_contacts_docx_view,
    ),
]
