from django.urls import URLPattern, URLResolver, path

from core.views.person.person_add_view import person_add_view
from core.views.person.person_edit_view import person_edit_view
from core.views.person.person_view import person_view

urlpatterns_person: list[URLPattern | URLResolver] = [
    path(name="person", route="person", view=person_view),
    path(name="person_new", route="person/new", view=person_add_view),
    path(name="person_edit", route="person/edit/<int:model_id>", view=person_edit_view),
]
