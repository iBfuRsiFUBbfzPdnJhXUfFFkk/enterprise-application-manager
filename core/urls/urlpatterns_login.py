from django.urls import URLPattern, URLResolver, path

from core.views.login.login_view import login_view

urlpatterns_login: list[URLPattern | URLResolver] = [
    path(name="login", route="login/", view=login_view),
]
