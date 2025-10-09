from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.person.person_add_view import person_add_view
from core.views.person.person_delete_view import person_delete_view
from core.views.person.person_detail_view import person_detail_view
from core.views.person.person_edit_view import person_edit_view
from core.views.person.person_view import person_view

urlpatterns_person: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name="person",
    view=person_view,
    view_edit=person_edit_view,
    view_new=person_add_view,
)

# Add detail view
urlpatterns_person.append(
    path(name="person_detail", route="person/<int:model_id>/", view=person_detail_view)
)

# Add delete view
urlpatterns_person.append(
    path(name="person_delete", route="person/delete/<int:model_id>/", view=person_delete_view)
)
