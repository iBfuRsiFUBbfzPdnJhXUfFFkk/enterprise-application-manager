from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.data_use_exception import (
    data_use_exception_add_view,
    data_use_exception_delete_view,
    data_use_exception_detail_view,
    data_use_exception_edit_view,
    data_use_exception_view,
)

urlpatterns_data_use_exception: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='data_use_exception',
    view=data_use_exception_view,
    view_edit=data_use_exception_edit_view,
    view_new=data_use_exception_add_view,
)

# Add detail view
urlpatterns_data_use_exception.append(
    path(name='data_use_exception_detail', route='data_use_exception/<int:model_id>/', view=data_use_exception_detail_view)
)

# Add delete view
urlpatterns_data_use_exception.append(
    path(name='data_use_exception_delete', route='data_use_exception/delete/<int:model_id>/', view=data_use_exception_delete_view)
)
