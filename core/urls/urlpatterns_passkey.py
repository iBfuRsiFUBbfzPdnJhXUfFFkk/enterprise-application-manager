from django.urls import URLPattern, path

from core.views.passkey.passkey_authentication_begin_view import passkey_authentication_begin_view
from core.views.passkey.passkey_authentication_complete_view import passkey_authentication_complete_view
from core.views.passkey.passkey_delete_view import passkey_delete_view
from core.views.passkey.passkey_management_view import passkey_management_view
from core.views.passkey.passkey_registration_begin_view import passkey_registration_begin_view
from core.views.passkey.passkey_registration_complete_view import passkey_registration_complete_view
from core.views.passkey.passkey_rename_view import passkey_rename_view

# Public passkey authentication endpoints (no login required)
urlpatterns_passkey_public: list[URLPattern] = [
    path(
        route='passkey-auth/begin/',
        view=passkey_authentication_begin_view,
        name='passkey_authentication_begin',
    ),
    path(
        route='passkey-auth/complete/',
        view=passkey_authentication_complete_view,
        name='passkey_authentication_complete',
    ),
]

# Authenticated passkey management endpoints
urlpatterns_passkey_authenticated: list[URLPattern] = [
    path(route='passkey/manage/', view=passkey_management_view, name='passkey_management'),
    path(
        route='passkey/register/begin/',
        view=passkey_registration_begin_view,
        name='passkey_registration_begin',
    ),
    path(
        route='passkey/register/complete/',
        view=passkey_registration_complete_view,
        name='passkey_registration_complete',
    ),
    path(route='passkey/delete/<uuid:passkey_uuid>/', view=passkey_delete_view, name='passkey_delete'),
    path(route='passkey/rename/<uuid:passkey_uuid>/', view=passkey_rename_view, name='passkey_rename'),
]
