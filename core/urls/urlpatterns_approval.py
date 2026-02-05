from django.urls import URLPattern, URLResolver, path

from core.views.approval.approval_add_view import approval_add_view
from core.views.approval.approval_detail_view import approval_detail_view
from core.views.approval.approval_edit_view import approval_edit_view
from core.views.approval.approval_update_add_ajax_view import approval_update_add_ajax_view
from core.views.approval.approval_update_delete_ajax_view import approval_update_delete_ajax_view
from core.views.approval.approval_update_edit_ajax_view import approval_update_edit_ajax_view
from core.views.approval.approval_view import approval_view


urlpatterns_approval: list[URLPattern | URLResolver] = [
    path("approval/", approval_view, name="approval"),
    path("approval/edit/<int:model_id>/", approval_edit_view, name="approval_edit"),
    path("approval/new/", approval_add_view, name="approval_new"),
    path("approval/<int:model_id>/detail/", approval_detail_view, name="approval_detail"),
    path("approval/<int:model_id>/update/add/", approval_update_add_ajax_view, name="approval_update_add"),
    path("approval/update/<int:update_id>/edit/", approval_update_edit_ajax_view, name="approval_update_edit"),
    path("approval/update/<int:update_id>/delete/", approval_update_delete_ajax_view, name="approval_update_delete"),
]
