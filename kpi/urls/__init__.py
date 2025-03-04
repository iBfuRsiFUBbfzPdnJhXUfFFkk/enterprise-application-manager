from django.urls import path, URLPattern, URLResolver

from kpi.views.kpi_home_view import kpi_home_view

urlpatterns: list[URLPattern | URLResolver] = [
    path(name='kpi_home', route='', view=kpi_home_view),
]
