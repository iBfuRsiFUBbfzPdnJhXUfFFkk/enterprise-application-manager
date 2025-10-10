from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.data_point import (
    data_point_add_view,
    data_point_delete_view,
    data_point_detail_view,
    data_point_edit_view,
    data_point_view,
)

urlpatterns_data_point: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='data_point',
    view=data_point_view,
    view_edit=data_point_edit_view,
    view_new=data_point_add_view,
)

# Add detail view
urlpatterns_data_point.append(
    path(name='data_point_detail', route='data_point/<int:model_id>/', view=data_point_detail_view)
)

# Add delete view
urlpatterns_data_point.append(
    path(name='data_point_delete', route='data_point/delete/<int:model_id>/', view=data_point_delete_view)
)
