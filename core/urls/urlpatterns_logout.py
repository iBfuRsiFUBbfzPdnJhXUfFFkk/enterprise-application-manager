from django.urls import URLPattern, URLResolver, path

from core.views.logout.logout_view import logout_view

urlpatterns_logout: list[URLPattern | URLResolver] = [
    path(name="logout", route="logout/", view=logout_view),
]
