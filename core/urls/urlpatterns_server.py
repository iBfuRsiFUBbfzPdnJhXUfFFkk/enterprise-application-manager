from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.server import (
    server_add_view,
    server_delete_view,
    server_detail_view,
    server_edit_view,
    server_view,
)

urlpatterns_server: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='server',
    view=server_view,
    view_edit=server_edit_view,
    view_new=server_add_view,
)

# Add detail view
urlpatterns_server.append(
    path(name='server_detail', route='server/<int:model_id>/', view=server_detail_view)
)

# Add delete view
urlpatterns_server.append(
    path(name='server_delete', route='server/delete/<int:model_id>/', view=server_delete_view)
)
