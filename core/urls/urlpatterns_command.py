from django.urls import URLPattern, URLResolver, path

from core.views.command import (
    command_add_view,
    command_delete_view,
    command_detail_view,
    command_edit_view,
    command_run_view,
    command_view,
)

urlpatterns_command: list[URLPattern | URLResolver] = [
    path("command/", command_view, name="command"),
    path("command/edit/<int:model_id>/", command_edit_view, name="command_edit"),
    path("command/new/", command_add_view, name="command_new"),
    path("command/<int:model_id>/", command_detail_view, name="command_detail"),
    path("command/delete/<int:model_id>/", command_delete_view, name="command_delete"),
    path("command/run/<int:model_id>/", command_run_view, name="command_run"),
]
