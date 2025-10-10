from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.client import (
    client_add_view,
    client_delete_view,
    client_detail_view,
    client_edit_view,
    client_view,
)

urlpatterns_client: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='client',
    view=client_view,
    view_edit=client_edit_view,
    view_new=client_add_view,
)

# Add detail view
urlpatterns_client.append(
    path(name='client_detail', route='client/<int:model_id>/', view=client_detail_view)
)

# Add delete view
urlpatterns_client.append(
    path(name='client_delete', route='client/delete/<int:model_id>/', view=client_delete_view)
)
