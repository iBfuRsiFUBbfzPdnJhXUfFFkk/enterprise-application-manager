from django.urls import path, URLPattern, URLResolver

from kpi.ajax.chart_data.kpi_chart_data_for_developer_ajax_view import kpi_chart_data_for_developer_ajax_view
from kpi.views.dashboard.kpi_dashboard_view import kpi_dashboard_view
from kpi.views.developer.kpi_developer_view import kpi_developer_view
from kpi.views.developer.kpi_developers_view import kpi_developers_view
from kpi.views.kpi_sprint_export_view import kpi_sprint_export_view
from kpi.views.sprint.kpi_sprint_view import kpi_sprint_view
from kpi.views.sprint.kpi_sprints_view import kpi_sprints_view

urlpatterns_kpi: list[URLPattern | URLResolver] = [
    path(
        name='kpi_chart_data_for_developer_ajax',
        route='chart-data/<uuid:uuid>/',
        view=kpi_chart_data_for_developer_ajax_view
    ),
    path(name='kpi_dashboard', route='dashboard/', view=kpi_dashboard_view),
    path(name='kpi_developer', route='<uuid:uuid>/', view=kpi_developer_view),
    path(name='kpi_developers', route='developer/', view=kpi_developers_view),
    path(name='kpi_sprint', route='sprints/<uuid:uuid>/', view=kpi_sprint_view),
    path(name='kpi_sprint_export', route='sprints/<uuid:uuid>/export/', view=kpi_sprint_export_view),
    path(name='kpi_sprints', route='sprints/', view=kpi_sprints_view),
]
