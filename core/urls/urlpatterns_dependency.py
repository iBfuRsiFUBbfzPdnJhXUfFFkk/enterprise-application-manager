from django.urls import URLPattern, URLResolver, path

from core.views.dependency.dependency_add_view import dependency_add_view
from core.views.dependency.dependency_edit_view import dependency_edit_view
from core.views.dependency.dependency_view import dependency_view

urlpatterns_dependency: list[URLPattern | URLResolver] = [
    path("dependency/", dependency_view, name="dependency"),
    path("dependency/edit/<int:model_id>/", dependency_edit_view, name="dependency_edit"),
    path("dependency/new/", dependency_add_view, name="dependency_new"),
]
