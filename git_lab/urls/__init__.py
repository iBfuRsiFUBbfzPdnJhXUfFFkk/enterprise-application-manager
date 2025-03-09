from django.urls import path, URLPattern, URLResolver

from git_lab.api.git_lab_issues_api import git_lab_issues_api
from git_lab.api.git_lab_merge_requests_api import git_lab_merge_requests_api
from git_lab.api.git_lab_users_api import git_lab_users_api
from git_lab.api.git_lab_groups_api import git_lab_groups_api
from git_lab.api.git_lab_projects_api import git_lab_projects_api

app_name: str = 'git_lab'

urlpatterns: list[URLPattern | URLResolver] = [
    path(name='git_lab_groups', route='group/', view=git_lab_groups_api),
    path(name='git_lab_issues', route='issue/', view=git_lab_issues_api),
    path(name='git_lab_merge_requests', route='merge-request/', view=git_lab_merge_requests_api),
    path(name='git_lab_projects', route='project/', view=git_lab_projects_api),
    path(name='git_lab_users', route='user/', view=git_lab_users_api),
]
