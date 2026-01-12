from django.urls import URLPattern, URLResolver, path

from core.views.tool import (
    tool_add_view,
    tool_delete_view,
    tool_detail_view,
    tool_edit_view,
    tool_view,
)

urlpatterns_tool: list[URLPattern | URLResolver] = [
    path("tool/", tool_view, name="tool"),
    path("tool/edit/<int:model_id>/", tool_edit_view, name="tool_edit"),
    path("tool/new/", tool_add_view, name="tool_new"),
    path("tool/<int:model_id>/", tool_detail_view, name="tool_detail"),
    path("tool/delete/<int:model_id>/", tool_delete_view, name="tool_delete"),
]
