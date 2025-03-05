from django.urls import URLPattern, URLResolver, path

from core.views.this_api.this_api_create_sprint_kpis_view import this_api_create_sprint_kpis_view
from core.views.this_api.this_api_sync_gitlab_users_view import this_api_sync_gitlab_users_view
from core.views.this_api.this_api_sync_git_lab_view.this_api_sync_git_lab_view import this_api_sync_git_lab_view


urlpatterns_this_api: list[URLPattern | URLResolver] = [
    path(name="this_api_sync_git_lab", route="api/sync_git_lab/", view=this_api_sync_git_lab_view),
    path(name="this_api_create_sprint_kpis", route="api/create_sprint_kpis/", view=this_api_create_sprint_kpis_view),
    path(name="this_api_sync_gitlab_users", route="api/sync_gitlab_users/", view=this_api_sync_gitlab_users_view),
]
