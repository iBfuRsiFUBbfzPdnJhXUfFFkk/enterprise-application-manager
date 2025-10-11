from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.organization import (
    organization_add_view,
    organization_delete_view,
    organization_detail_view,
    organization_edit_view,
    organization_view,
)

urlpatterns_organization: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='organization',
    view=organization_view,
    view_edit=organization_edit_view,
    view_new=organization_add_view,
)

# Add detail view
urlpatterns_organization.append(
    path(name='organization_detail', route='organization/<int:model_id>/', view=organization_detail_view)
)

# Add delete view
urlpatterns_organization.append(
    path(name='organization_delete', route='organization/delete/<int:model_id>/', view=organization_delete_view)
)
