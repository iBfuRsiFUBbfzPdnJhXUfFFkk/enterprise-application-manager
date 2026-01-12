from django.urls import URLPattern, URLResolver, path

from core.views.login_credential import (
    login_credential_add_view,
    login_credential_delete_view,
    login_credential_detail_view,
    login_credential_edit_view,
    login_credential_view,
)

urlpatterns_login_credential: list[URLPattern | URLResolver] = [
    path("login_credential/", login_credential_view, name="login_credential"),
    path("login_credential/edit/<int:model_id>/", login_credential_edit_view, name="login_credential_edit"),
    path("login_credential/new/", login_credential_add_view, name="login_credential_new"),
    path("login_credential/<int:model_id>/", login_credential_detail_view, name="login_credential_detail"),
    path("login_credential/delete/<int:model_id>/", login_credential_delete_view, name="login_credential_delete"),
]
