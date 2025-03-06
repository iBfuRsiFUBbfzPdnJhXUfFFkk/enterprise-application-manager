from django.urls import path, URLPattern, URLResolver

from kpi.ajax.chart_data.ajax_get_chart_data_for_dashboard import ajax_get_chart_data_for_dashboard
from kpi.ajax.chart_data.ajax_get_chart_data_for_dashboard_user import ajax_get_chart_data_for_dashboard_user
from kpi.ajax.chart_data.ajax_get_chart_data_for_self import ajax_get_chart_data_for_self
from kpi.ajax.chart_data.ajax_get_chart_data_for_user import ajax_get_chart_data_for_user
from kpi.views.kpi_dashboard_view import kpi_dashboard_view
from kpi.views.kpi_home_view import kpi_home_view
from kpi.views.kpi_person_view import kpi_person_view
from kpi.views.kpi_sprint_view import kpi_sprint_view
from kpi.views.kpi_sprints_view import kpi_sprints_view

app_name: str = 'kpi'

urlpatterns: list[URLPattern | URLResolver] = [
    path(name='kpi_home', route='', view=kpi_home_view),
    path(name='kpi_dashboard', route='dashboard/', view=kpi_dashboard_view),
    path(name='kpi_person', route='<uuid:uuid>/', view=kpi_person_view),
    path(name='kpi_sprints', route='sprints/', view=kpi_sprints_view),
    path(name='kpi_sprint', route='sprints/<uuid:uuid>/', view=kpi_sprint_view),
    path(name='ajax_get_chart_data_for_self', route='chart-data/self/', view=ajax_get_chart_data_for_self),
    path(name='ajax_get_chart_data_for_user', route='chart-data/<uuid:uuid>/', view=ajax_get_chart_data_for_user),
    path(name='ajax_get_chart_data_for_dashboard', route='chart-data/dashboard/', view=ajax_get_chart_data_for_dashboard),
    path(name='ajax_get_chart_data_for_dashboard_user', route='chart-data/dashboard/<uuid:uuid>/', view=ajax_get_chart_data_for_dashboard_user),
]
