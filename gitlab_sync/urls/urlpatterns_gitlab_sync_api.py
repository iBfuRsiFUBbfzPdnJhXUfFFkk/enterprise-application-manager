from django.urls import path

from gitlab_sync.apis import gitlab_sync_pipelines_api, gitlab_sync_projects_api
from gitlab_sync.views import gitlab_sync_dashboard_view

urlpatterns_gitlab_sync = [
    path(
        name="gitlab_sync_dashboard",
        route="",
        view=gitlab_sync_dashboard_view,
    ),
]

urlpatterns_gitlab_sync_api = [
    path(
        name="gitlab_sync_api_projects",
        route="project/",
        view=gitlab_sync_projects_api,
    ),
    path(
        name="gitlab_sync_api_pipelines",
        route="pipeline/",
        view=gitlab_sync_pipelines_api,
    ),
]
