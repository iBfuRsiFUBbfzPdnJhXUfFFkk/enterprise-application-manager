from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.sprint import (
    sprint_add_view,
    sprint_delete_view,
    sprint_detail_view,
    sprint_edit_view,
    sprint_view,
)

urlpatterns_sprint: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='sprint',
    view=sprint_view,
    view_edit=sprint_edit_view,
    view_new=sprint_add_view,
)

# Add detail view
urlpatterns_sprint.append(
    path(name='sprint_detail', route='sprint/<int:model_id>/', view=sprint_detail_view)
)

# Add delete view
urlpatterns_sprint.append(
    path(name='sprint_delete', route='sprint/delete/<int:model_id>/', view=sprint_delete_view)
)
