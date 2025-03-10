from django.urls import URLPattern, URLResolver, path

from scrum.apis.scrum_sprints_api import scrum_sprints_api

urlpatterns_scrum_api: list[URLPattern | URLResolver] = [
    path(name="scrum_api_sprints", route="sprint/", view=scrum_sprints_api),
]
