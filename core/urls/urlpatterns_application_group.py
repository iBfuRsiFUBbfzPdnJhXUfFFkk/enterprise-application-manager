from django.urls import URLPattern, URLResolver

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.application_group.application_group_add_view import application_group_add_view
from core.views.application_group.application_group_edit_view import application_group_edit_view
from core.views.application_group.application_group_view import application_group_view

urlpatterns_application_group: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name="application_group",
    view=application_group_view,
    view_edit=application_group_edit_view,
    view_new=application_group_add_view,
)
