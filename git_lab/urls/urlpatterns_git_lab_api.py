from django.urls import URLPattern, URLResolver, path

from git_lab.apis.git_lab_changes_api import git_lab_changes_api
from git_lab.apis.git_lab_discussions_api import git_lab_discussions_api
from git_lab.apis.git_lab_discussions_api_v2 import git_lab_discussions_api_v2
from git_lab.apis.git_lab_groups_api import git_lab_groups_api
from git_lab.apis.git_lab_issues_api import git_lab_issues_api
from git_lab.apis.git_lab_iterations_api import git_lab_iterations_api
from git_lab.apis.git_lab_merge_requests_api import git_lab_merge_requests_api
from git_lab.apis.git_lab_projects_api import git_lab_projects_api
from git_lab.apis.git_lab_users_api import git_lab_users_api

urlpatterns_git_lab_api: list[URLPattern | URLResolver] = [
    path(name='git_lab_api_changes', route='change/', view=git_lab_changes_api),
    path(name='git_lab_api_discussions', route='discussion/', view=git_lab_discussions_api_v2),
    path(name='git_lab_api_groups', route='group/', view=git_lab_groups_api),
    path(name='git_lab_api_issues', route='issue/', view=git_lab_issues_api),
    path(name='git_lab_api_iterations', route='iteration/', view=git_lab_iterations_api),
    path(name='git_lab_api_merge_requests', route='merge-request/', view=git_lab_merge_requests_api),
    path(name='git_lab_api_projects', route='project/', view=git_lab_projects_api),
    path(name='git_lab_api_users', route='user/', view=git_lab_users_api),
]