from django.urls import URLPattern, URLResolver, path

from core.views.application_group.application_group_add_view import application_group_add_view
from core.views.application_group.application_group_edit_view import application_group_edit_view
from core.views.application_group.application_group_view import application_group_view

urlpatterns_application_group: list[URLPattern | URLResolver] = [
    path(name="application_group", route="application_group", view=application_group_view),
    path(name="application_group_new", route="application_group/new", view=application_group_add_view),
    path(name="application_group_edit", route="application_group/edit/<int:model_id>",
         view=application_group_edit_view),
]
