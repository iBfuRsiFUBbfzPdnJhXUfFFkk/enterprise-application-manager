from django.urls import URLPattern, path

from core.views.server_configuration import server_configuration_view

urlpatterns_server_configuration: list[URLPattern] = [
    path(route='server-configuration/', view=server_configuration_view, name='server_configuration'),
]
