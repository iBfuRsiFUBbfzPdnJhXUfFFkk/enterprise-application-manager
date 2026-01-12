from django.urls import URLPattern, URLResolver, path

from core.views.api import (
    api_add_view,
    api_delete_view,
    api_detail_view,
    api_edit_view,
    api_view,
)
from core.views.api_authentication import (
    api_authentication_add_view,
    api_authentication_delete_view,
    api_authentication_edit_view,
)
from core.views.api_request import (
    api_request_add_view,
    api_request_delete_view,
    api_request_detail_view,
    api_request_edit_view,
    api_request_execute_view,
    api_request_view,
)

urlpatterns_api_resources: list[URLPattern | URLResolver] = [
    path("api/", api_view, name="api"),
    path("api/edit/<int:model_id>/", api_edit_view, name="api_edit"),
    path("api/new/", api_add_view, name="api_new"),
    path("api/<int:model_id>/", api_detail_view, name="api_detail"),
    path("api/delete/<int:model_id>/", api_delete_view, name="api_delete"),
    # APIAuthentication routes
    path(
        "api/<int:api_id>/authentication/new/",
        api_authentication_add_view,
        name="api_authentication_new",
    ),
    path(
        "api/authentication/edit/<int:model_id>/",
        api_authentication_edit_view,
        name="api_authentication_edit",
    ),
    path(
        "api/authentication/delete/<int:model_id>/",
        api_authentication_delete_view,
        name="api_authentication_delete",
    ),
    # APIRequest routes
    path("api_request/", api_request_view, name="api_request"),
    path("api_request/edit/<int:model_id>/", api_request_edit_view, name="api_request_edit"),
    path("api_request/new/", api_request_add_view, name="api_request_new"),
    path("api-request/<int:model_id>/", api_request_detail_view, name="api_request_detail"),
    path("api-request/delete/<int:model_id>/", api_request_delete_view, name="api_request_delete"),
    path("api-request/<int:request_id>/execute/", api_request_execute_view, name="api_request_execute"),
]
