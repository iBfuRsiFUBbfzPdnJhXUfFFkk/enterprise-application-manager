from django.urls import URLPattern, URLResolver, path

from core.views.dependency.dependency_add_view import dependency_add_view
from core.views.dependency.dependency_edit_view import dependency_edit_view
from core.views.dependency.dependency_view import dependency_view

urlpatterns_dependency: list[URLPattern | URLResolver] = [
    path(name="dependency", route="dependency", view=dependency_view),
    path(name="dependency_new", route="dependency/new", view=dependency_add_view),
    path(name="dependency_edit", route="dependency/edit/<int:model_id>", view=dependency_edit_view),
]
