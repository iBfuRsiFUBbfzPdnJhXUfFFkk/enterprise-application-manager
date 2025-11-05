from gitlab_sync.views.gitlab_sync_dashboard_view import gitlab_sync_dashboard_view
from gitlab_sync.views.gitlab_sync_job_history_view import gitlab_sync_job_history_view
from gitlab_sync.views.gitlab_sync_link_projects_view import (
    gitlab_sync_link_projects_view,
)
from gitlab_sync.views.gitlab_sync_link_users_view import gitlab_sync_link_users_view

__all__ = [
    "gitlab_sync_dashboard_view",
    "gitlab_sync_job_history_view",
    "gitlab_sync_link_projects_view",
    "gitlab_sync_link_users_view",
]
