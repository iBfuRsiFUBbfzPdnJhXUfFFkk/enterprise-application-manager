from django.urls import URLPattern, URLResolver, path

from core.views.this_api.this_api_sync_git_lab_view.this_api_sync_git_lab_view import this_api_sync_git_lab_view

urlpatterns_this_api: list[URLPattern | URLResolver] = [
    path(name="this_api_sync_git_lab", route="api/sync_git_lab/", view=this_api_sync_git_lab_view),
]
