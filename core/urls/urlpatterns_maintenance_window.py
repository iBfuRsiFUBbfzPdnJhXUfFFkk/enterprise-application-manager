from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.maintenance_window import (
    maintenance_window_add_view,
    maintenance_window_delete_view,
    maintenance_window_detail_view,
    maintenance_window_edit_view,
    maintenance_window_view,
)

urlpatterns_maintenance_window: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='maintenance_window',
    view=maintenance_window_view,
    view_edit=maintenance_window_edit_view,
    view_new=maintenance_window_add_view,
)

# Add detail view
urlpatterns_maintenance_window.append(
    path(
        name='maintenance_window_detail',
        route='maintenance-window/<int:model_id>/',
        view=maintenance_window_detail_view
    )
)

# Add delete view
urlpatterns_maintenance_window.append(
    path(
        name='maintenance_window_delete',
        route='maintenance-window/delete/<int:model_id>/',
        view=maintenance_window_delete_view
    )
)
