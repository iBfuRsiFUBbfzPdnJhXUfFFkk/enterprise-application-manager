from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.secret import (
    secret_add_view,
    secret_edit_view,
    secret_quick_add_view,
    secret_view,
)

urlpatterns_secret: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name="secret",
    view=secret_view,
    view_edit=secret_edit_view,
    view_new=secret_add_view,
)

urlpatterns_secret.append(
    path(
        name='secret_quick_add',
        route='secret/quick-add/',
        view=secret_quick_add_view,
    )
)
