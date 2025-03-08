from django.urls import path, URLPattern, URLResolver

from git_lab.api.git_lab_group_members_api import git_lab_group_members_api

app_name: str = 'git_lab'

urlpatterns: list[URLPattern | URLResolver] = [
    path(name='git_lab_group_members', route='group/member/', view=git_lab_group_members_api),
]
