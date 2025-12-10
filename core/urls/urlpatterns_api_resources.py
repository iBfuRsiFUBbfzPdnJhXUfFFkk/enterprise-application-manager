from django.urls import URLPattern, URLResolver, path
from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.api import (
    api_add_view,
    api_delete_view,
    api_detail_view,
    api_edit_view,
    api_view,
)
from core.views.api_request import (
    api_request_add_view,
    api_request_delete_view,
    api_request_detail_view,
    api_request_edit_view,
    api_request_view,
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

# APIRequest routes
urlpatterns_api_resources.extend(
    create_generic_urlpatterns(
        name='api_request',
        view=api_request_view,
        view_edit=api_request_edit_view,
        view_new=api_request_add_view,
    )
)

urlpatterns_api_resources.append(
    path(
        name='api_request_detail',
        route='api-request/<int:model_id>/',
        view=api_request_detail_view,
    )
)

urlpatterns_api_resources.append(
    path(
        name='api_request_delete',
        route='api-request/delete/<int:model_id>/',
        view=api_request_delete_view,
    )
)
