from typing import Callable

from django.http import HttpRequest, HttpResponse
from django.urls import URLPattern, URLResolver, path


def create_generic_urlpatterns(
        name: str | None = None,
        view: Callable[[HttpRequest], HttpResponse] | None = None,
        view_edit: Callable[[HttpRequest, int], HttpResponse] | None = None,
        view_new: Callable[[HttpRequest], HttpResponse] | None = None,
) -> list[URLPattern | URLResolver]:
    if name is None:
        return []
    patterns: list[URLPattern | URLResolver] = []
    if view is not None:
        patterns.append(path(name=name, route=f"{name}/", view=view))
    if view_edit is not None:
        patterns.append(path(name=f"{name}_edit", route=f"{name}/edit/<int:model_id>/", view=view_edit))
    if view_new is not None:
        patterns.append(path(name=f"{name}_new", route=f"{name}/new/", view=view_new))
    return patterns
