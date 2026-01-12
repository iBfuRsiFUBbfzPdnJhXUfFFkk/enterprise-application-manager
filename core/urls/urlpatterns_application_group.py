from django.urls import URLPattern, URLResolver, path

from core.views.application_group.application_group_add_view import application_group_add_view
from core.views.application_group.application_group_delete_view import application_group_delete_view
from core.views.application_group.application_group_detail_view import application_group_detail_view
from core.views.application_group.application_group_edit_view import application_group_edit_view
from core.views.application_group.application_group_view import application_group_view

urlpatterns_application_group: list[URLPattern | URLResolver] = [
    path("application_group/", application_group_view, name="application_group"),
    path("application_group/edit/<int:model_id>/", application_group_edit_view, name="application_group_edit"),
    path("application_group/new/", application_group_add_view, name="application_group_new"),
    path("application_group/<int:model_id>/", application_group_detail_view, name="application_group_detail"),
    path("application_group/delete/<int:model_id>/", application_group_delete_view, name="application_group_delete"),
]
