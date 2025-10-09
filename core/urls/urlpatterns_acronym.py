from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.acronym.acronym_add_view import acronym_add_view
from core.views.acronym.acronym_delete_view import acronym_delete_view
from core.views.acronym.acronym_detail_view import acronym_detail_view
from core.views.acronym.acronym_edit_view import acronym_edit_view
from core.views.acronym.acronym_view import acronym_view

urlpatterns_acronym: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name="acronym",
    view=acronym_view,
    view_edit=acronym_edit_view,
    view_new=acronym_add_view,
)

# Add detail view
urlpatterns_acronym.append(
    path(name="acronym_detail", route="acronym/<int:model_id>/", view=acronym_detail_view)
)

# Add delete view
urlpatterns_acronym.append(
    path(name="acronym_delete", route="acronym/delete/<int:model_id>/", view=acronym_delete_view)
)
