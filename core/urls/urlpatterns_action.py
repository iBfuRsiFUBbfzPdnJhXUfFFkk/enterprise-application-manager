from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.action.action_add_view import action_add_view
from core.views.action.action_detail_view import action_detail_view
from core.views.action.action_edit_view import action_edit_view
from core.views.action.action_run_view import action_run_view
from core.views.action.action_view import action_view

urlpatterns_action: list[URLPattern | URLResolver] = [
    *create_generic_urlpatterns(
        name="action",
        view=action_view,
        view_edit=action_edit_view,
        view_new=action_add_view,
    ),
    path(name="action_detail", route="action/<int:model_id>/", view=action_detail_view),
    path(name="action_run", route="action/run/<int:model_id>/", view=action_run_view)
]
