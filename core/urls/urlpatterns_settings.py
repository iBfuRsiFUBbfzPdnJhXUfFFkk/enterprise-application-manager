from django.urls import URLPattern, path

from core.views.settings import settings_view

urlpatterns_settings: list[URLPattern] = [
    path(route='settings/', view=settings_view, name='settings'),
]
