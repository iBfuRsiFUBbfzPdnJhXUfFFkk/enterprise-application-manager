from django.urls import URLPattern, path

from core.views.profile.profile_view import profile_view

urlpatterns_profile: list[URLPattern] = [
    path(route='profile/', view=profile_view, name='profile'),
]
