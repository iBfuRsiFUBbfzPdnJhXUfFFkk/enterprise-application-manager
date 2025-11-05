from django.urls import path

from gitlab_sync.apis import (
    gitlab_sync_cancel_job_api,
    gitlab_sync_groups_api,
    gitlab_sync_job_status_api,
    gitlab_sync_link_user_api,
    gitlab_sync_pipelines_api,
    gitlab_sync_projects_api,
    gitlab_sync_users_api,
)
from gitlab_sync.views import (
    gitlab_sync_dashboard_view,
    gitlab_sync_job_history_view,
    gitlab_sync_link_users_view,
)

urlpatterns_gitlab_sync = [
    path(
        name="gitlab_sync_dashboard",
        route="",
        view=gitlab_sync_dashboard_view,
    ),
    path(
        name="gitlab_sync_link_users",
        route="link-users/",
        view=gitlab_sync_link_users_view,
    ),
    path(
        name="gitlab_sync_job_history",
        route="job-history/",
        view=gitlab_sync_job_history_view,
    ),
]

urlpatterns_gitlab_sync_api = [
    path(
        name="gitlab_sync_api_groups",
        route="group/",
        view=gitlab_sync_groups_api,
    ),
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
    path(
        name="gitlab_sync_api_users",
        route="user/",
        view=gitlab_sync_users_api,
    ),
    path(
        name="gitlab_sync_api_link_user",
        route="link-user/",
        view=gitlab_sync_link_user_api,
    ),
    path(
        name="gitlab_sync_api_job_status",
        route="job/<int:job_id>/",
        view=gitlab_sync_job_status_api,
    ),
    path(
        name="gitlab_sync_api_cancel_job",
        route="job/<int:job_id>/cancel/",
        view=gitlab_sync_cancel_job_api,
    ),
]
