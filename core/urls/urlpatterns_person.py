from django.urls import URLPattern, URLResolver

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.person.person_add_view import person_add_view
from core.views.person.person_edit_view import person_edit_view
from core.views.person.person_view import person_view

urlpatterns_person: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name="person",
    view=person_view,
    view_edit=person_edit_view,
    view_new=person_add_view,
)
