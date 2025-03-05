from django.urls import path, URLPattern, URLResolver

from kpi.ajax.ajax_get_chart_data_for_user import ajax_get_chart_data_for_user
from kpi.views.kpi_home_view import kpi_home_view

app_name: str = 'kpi'

urlpatterns: list[URLPattern | URLResolver] = [
    path(name='kpi_home', route='', view=kpi_home_view),
    path(name='ajax_get_chart_data_for_user', route='chart-data/<uuid:uuid>', view=ajax_get_chart_data_for_user),
]
