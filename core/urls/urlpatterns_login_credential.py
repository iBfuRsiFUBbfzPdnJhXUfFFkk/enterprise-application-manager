from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.login_credential import (
    login_credential_add_view,
    login_credential_delete_view,
    login_credential_detail_view,
    login_credential_edit_view,
    login_credential_view,
)

urlpatterns_login_credential: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='login_credential',
    view=login_credential_view,
    view_edit=login_credential_edit_view,
    view_new=login_credential_add_view,
)

# Add detail view
urlpatterns_login_credential.append(
    path(name='login_credential_detail', route='login_credential/<int:model_id>/', view=login_credential_detail_view)
)

# Add delete view
urlpatterns_login_credential.append(
    path(name='login_credential_delete', route='login_credential/delete/<int:model_id>/', view=login_credential_delete_view)
)
