from django.urls import URLPattern, URLResolver

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.dependency.dependency_add_view import dependency_add_view
from core.views.dependency.dependency_edit_view import dependency_edit_view
from core.views.dependency.dependency_view import dependency_view

urlpatterns_dependency: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name="dependency",
    view=dependency_view,
    view_edit=dependency_edit_view,
    view_new=dependency_add_view,
)
