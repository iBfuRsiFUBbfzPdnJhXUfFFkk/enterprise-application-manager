from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.role import (
    role_add_view,
    role_delete_view,
    role_detail_view,
    role_edit_view,
    role_view,
)

urlpatterns_role: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='role',
    view=role_view,
    view_edit=role_edit_view,
    view_new=role_add_view,
)

# Add detail view
urlpatterns_role.append(
    path(name='role_detail', route='role/<int:model_id>/', view=role_detail_view)
)

# Add delete view
urlpatterns_role.append(
    path(name='role_delete', route='role/delete/<int:model_id>/', view=role_delete_view)
)
