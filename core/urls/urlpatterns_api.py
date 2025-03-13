from django.urls import URLPattern, URLResolver, include, path

from git_lab.urls.urlpatterns_git_lab_api import urlpatterns_git_lab_api
from kpi.urls.urlpatterns_kpi_api import urlpatterns_kpi_api
from scrum.urls.urlpatterns_scrum_api import urlpatterns_scrum_api

urlpatterns_api: list[URLPattern | URLResolver] = [
    path(name="api", route='api/', view=include(arg=[
        path(name="git_lab_api", route='git-lab/', view=include(arg=urlpatterns_git_lab_api)),
        path(name="kpi_api", route='kpi/', view=include(arg=urlpatterns_kpi_api)),
        path(name="scrum_api", route='scrum/', view=include(arg=urlpatterns_scrum_api)),
    ])),
]
