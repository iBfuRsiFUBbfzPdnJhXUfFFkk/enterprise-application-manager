from django.urls import URLPattern, URLResolver

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.acronym.acronym_add_view import acronym_add_view
from core.views.acronym.acronym_edit_view import acronym_edit_view
from core.views.acronym.acronym_view import acronym_view

urlpatterns_acronym: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name="acronym",
    view=acronym_view,
    view_edit=acronym_edit_view,
    view_new=acronym_add_view,
)
