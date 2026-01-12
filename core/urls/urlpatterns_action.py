from django.urls import URLPattern, URLResolver, path

from core.views.action.action_add_view import action_add_view
from core.views.action.action_detail_view import action_detail_view
from core.views.action.action_edit_view import action_edit_view
from core.views.action.action_run_view import action_run_view
from core.views.action.action_view import action_view

urlpatterns_action: list[URLPattern | URLResolver] = [
    path("action/", action_view, name="action"),
    path("action/edit/<int:model_id>/", action_edit_view, name="action_edit"),
    path("action/new/", action_add_view, name="action_new"),
    path("action/<int:model_id>/", action_detail_view, name="action_detail"),
    path("action/run/<int:model_id>/", action_run_view, name="action_run"),
]
