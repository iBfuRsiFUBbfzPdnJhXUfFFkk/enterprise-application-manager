from django.contrib.admin import site
from django.urls import URLPattern, URLResolver, path

from core.views import home_view, application_view, person_view, application_add_view, person_add_view, \
    application_edit_view, person_edit_view, database_add_view, \
    database_view, database_edit_view

urlpatterns: list[URLPattern | URLResolver] = [
    # HOME (INDEX)
    path(name="index", route="", view=home_view),
    path(name="home", route="home", view=home_view),

    # ADMIN
    path(name="admin", route="admin", view=site.urls),

    # APPLICATION
    path(name="application", route="application", view=application_view),
    path(name="application_new", route="application/new", view=application_add_view),
    path(name="application_edit", route="application/edit/<int:application_id>", view=application_edit_view),

    # PERSON
    path(name="person", route="person", view=person_view),
    path(name="person_new", route="person/new", view=person_add_view),
    path(name="person_edit", route="person/edit/<int:person_id>", view=person_edit_view),

    # DATABASE
    path(name="database", route="database", view=database_view),
    path(name="database_new", route="database/new", view=database_add_view),
    path(name="database_edit", route="database/edit/<int:database_id>", view=database_edit_view),
]
