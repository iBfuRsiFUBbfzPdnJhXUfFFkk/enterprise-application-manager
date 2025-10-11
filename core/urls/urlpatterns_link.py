from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.link import (
    link_add_view,
    link_delete_view,
    link_detail_view,
    link_edit_view,
    link_view,
)

urlpatterns_link: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='link',
    view=link_view,
    view_edit=link_edit_view,
    view_new=link_add_view,
)

# Add detail view
urlpatterns_link.append(
    path(name='link_detail', route='link/<int:model_id>/', view=link_detail_view)
)

# Add delete view
urlpatterns_link.append(
    path(name='link_delete', route='link/delete/<int:model_id>/', view=link_delete_view)
)
