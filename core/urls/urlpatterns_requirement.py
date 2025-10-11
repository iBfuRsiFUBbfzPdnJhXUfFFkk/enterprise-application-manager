from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.requirement import (
    requirement_add_view,
    requirement_delete_view,
    requirement_detail_view,
    requirement_edit_view,
    requirement_view,
)

urlpatterns_requirement: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='requirement',
    view=requirement_view,
    view_edit=requirement_edit_view,
    view_new=requirement_add_view,
)

# Add detail view
urlpatterns_requirement.append(
    path(name='requirement_detail', route='requirement/<int:model_id>/', view=requirement_detail_view)
)

# Add delete view
urlpatterns_requirement.append(
    path(name='requirement_delete', route='requirement/delete/<int:model_id>/', view=requirement_delete_view)
)
