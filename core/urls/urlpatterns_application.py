from django.urls import URLPattern, URLResolver

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.application.application_add_view import application_add_view
from core.views.application.application_edit_view import application_edit_view
from core.views.application.application_view import application_view

urlpatterns_application: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name="application",
    view=application_view,
    view_edit=application_edit_view,
    view_new=application_add_view,
)
