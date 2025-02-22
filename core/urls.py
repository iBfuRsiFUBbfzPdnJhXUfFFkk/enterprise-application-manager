from django.contrib.admin import site
from django.urls import URLPattern, URLResolver, path

from core.views import home_view, application_view, person_view, application_add_view, person_add_view, \
    person_added_view, application_added_view

urlpatterns: list[URLPattern | URLResolver] = [
    # HOME (INDEX)
    path(name="index", route="", view=home_view),
    path(name="home", route="home", view=home_view),

    # ADMIN
    path(name="admin", route="admin", view=site.urls),

    # APPLICATION
    path(name="application", route="application", view=application_view),
    path(name="application_new", route="application/new", view=application_add_view),
    path(name="application_added", route="application/added", view=application_added_view),

    # PERSON
    path(name="person", route="person", view=person_view),
    path(name="person_new", route="person/new", view=person_add_view),
    path(name="person_added", route="person/added", view=person_added_view),
]
