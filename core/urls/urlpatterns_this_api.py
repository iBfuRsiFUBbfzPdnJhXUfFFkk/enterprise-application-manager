from django.urls import URLPattern, URLResolver, path

from core.views.this_api.this_api_sync_gitlab_users_view import this_api_sync_gitlab_users_view

urlpatterns_this_api: list[URLPattern | URLResolver] = [
    path(name="this_api_sync_gitlab_users", route="api/sync_gitlab_users/", view=this_api_sync_gitlab_users_view),
]
