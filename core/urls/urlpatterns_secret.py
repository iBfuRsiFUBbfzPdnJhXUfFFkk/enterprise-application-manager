from django.urls import URLPattern, URLResolver

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.secret.secret_add_view import secret_add_view
from core.views.secret.secret_edit_view import secret_edit_view
from core.views.secret.secret_view import secret_view

urlpatterns_secret: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name="secret",
    view=secret_view,
    view_edit=secret_edit_view,
    view_new=secret_add_view,
)
