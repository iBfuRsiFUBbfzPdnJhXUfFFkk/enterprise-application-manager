from django.urls import URLPattern, URLResolver, path

from core.views.person.person_add_view import person_add_view
from core.views.person.person_delete_view import person_delete_view
from core.views.person.person_detail_view import person_detail_view
from core.views.person.person_edit_view import person_edit_view
from core.views.person.person_view import person_view

urlpatterns_person: list[URLPattern | URLResolver] = [
    path("person/", person_view, name="person"),
    path("person/edit/<int:model_id>/", person_edit_view, name="person_edit"),
    path("person/new/", person_add_view, name="person_new"),
    path("person/<int:model_id>/", person_detail_view, name="person_detail"),
    path("person/delete/<int:model_id>/", person_delete_view, name="person_delete"),
]
