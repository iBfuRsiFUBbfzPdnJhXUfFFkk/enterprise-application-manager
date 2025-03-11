from django.urls import URLPattern, URLResolver, include, path

from kpi.urls.urlpatterns_kpi_api import urlpatterns_kpi_api

urlpatterns_api: list[URLPattern | URLResolver] = [
    path(name="api", route='api/', view=include(arg=[
        path(name="kpi", route='kpi/', view=include(arg=[
            *urlpatterns_kpi_api
        ])),
    ])),
]
