from django.urls import URLPattern, URLResolver, path, include

from scrum.urls.urlpatterns_scrum_api import urlpatterns_scrum_api

urlpatterns_scrum: list[URLPattern | URLResolver] = [
    path(name="scrum_api", route='api/', view=include(arg=urlpatterns_scrum_api)),
]

urlpatterns: list[URLPattern | URLResolver] = urlpatterns_scrum
