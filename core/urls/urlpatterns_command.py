from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.command import (
    command_add_view,
    command_delete_view,
    command_detail_view,
    command_edit_view,
    command_run_view,
    command_view,
)

urlpatterns_command: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='command',
    view=command_view,
    view_edit=command_edit_view,
    view_new=command_add_view,
)

# Add detail view
urlpatterns_command.append(
    path(name='command_detail', route='command/<int:model_id>/', view=command_detail_view)
)

# Add delete view
urlpatterns_command.append(
    path(name='command_delete', route='command/delete/<int:model_id>/', view=command_delete_view)
)

# Add run view (for executing Python commands)
urlpatterns_command.append(
    path(name='command_run', route='command/run/<int:model_id>/', view=command_run_view)
)
