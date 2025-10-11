from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.tool import (
    tool_add_view,
    tool_delete_view,
    tool_detail_view,
    tool_edit_view,
    tool_view,
)

urlpatterns_tool: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='tool',
    view=tool_view,
    view_edit=tool_edit_view,
    view_new=tool_add_view,
)

# Add detail view
urlpatterns_tool.append(
    path(name='tool_detail', route='tool/<int:model_id>/', view=tool_detail_view)
)

# Add delete view
urlpatterns_tool.append(
    path(name='tool_delete', route='tool/delete/<int:model_id>/', view=tool_delete_view)
)
