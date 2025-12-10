from django.urls import URLPattern, URLResolver, path
from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.api import (
    api_add_view,
    api_delete_view,
    api_detail_view,
    api_edit_view,
    api_view,
)

urlpatterns_api_resources: list[URLPattern | URLResolver] = (
    create_generic_urlpatterns(
        name='api', view=api_view, view_edit=api_edit_view, view_new=api_add_view
    )
)

urlpatterns_api_resources.append(
    path(name='api_detail', route='api/<int:model_id>/', view=api_detail_view)
)

urlpatterns_api_resources.append(
    path(name='api_delete', route='api/delete/<int:model_id>/', view=api_delete_view)
)
