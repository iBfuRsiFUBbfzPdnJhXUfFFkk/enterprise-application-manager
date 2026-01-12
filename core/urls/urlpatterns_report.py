from django.urls import URLPattern, URLResolver, path

from core.views.report import (
    report_add_view,
    report_delete_view,
    report_detail_view,
    report_edit_view,
    report_view,
)

urlpatterns_report: list[URLPattern | URLResolver] = [
    path("report/", report_view, name="report"),
    path("report/edit/<int:model_id>/", report_edit_view, name="report_edit"),
    path("report/new/", report_add_view, name="report_new"),
    path("report/<int:model_id>/", report_detail_view, name="report_detail"),
    path("report/delete/<int:model_id>/", report_delete_view, name="report_delete"),
]
