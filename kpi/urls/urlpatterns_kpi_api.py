from django.urls import URLPattern, URLResolver, path

from kpi.apis.kpi_sprints_api import kpi_sprints_api

urlpatterns_kpi_api: list[URLPattern | URLResolver] = [
    path(name="kpi_api_sprints", route="sprint/", view=kpi_sprints_api),
]
