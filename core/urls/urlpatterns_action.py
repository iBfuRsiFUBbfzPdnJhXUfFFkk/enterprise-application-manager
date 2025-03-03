from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.action.action_run_view import action_run_view
from core.views.action.action_view import action_view

urlpatterns_action: list[URLPattern | URLResolver] = [
    *create_generic_urlpatterns(
        name="action",
        view=action_view,
        view_edit=None,
        view_new=None,
    ),
    path(name=f"action_run", route=f"action/run/<int:model_id>/", view=action_run_view)
]
