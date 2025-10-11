from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.report import (
    report_add_view,
    report_delete_view,
    report_detail_view,
    report_edit_view,
    report_view,
)

urlpatterns_report: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='report',
    view=report_view,
    view_edit=report_edit_view,
    view_new=report_add_view,
)

# Add detail view
urlpatterns_report.append(
    path(name='report_detail', route='report/<int:model_id>/', view=report_detail_view)
)

# Add delete view
urlpatterns_report.append(
    path(name='report_delete', route='report/delete/<int:model_id>/', view=report_delete_view)
)
