from django.urls import URLPattern, URLResolver, path

from core.views.hotfix import (
    hotfix_add_view,
    hotfix_delete_view,
    hotfix_detail_view,
    hotfix_edit_view,
    hotfix_view,
)

urlpatterns_hotfix: list[URLPattern | URLResolver] = [
    path("hotfix/", hotfix_view, name="hotfix"),
    path("hotfix/edit/<int:model_id>/", hotfix_edit_view, name="hotfix_edit"),
    path("hotfix/new/", hotfix_add_view, name="hotfix_new"),
    path("hotfix/<int:model_id>/", hotfix_detail_view, name="hotfix_detail"),
    path("hotfix/delete/<int:model_id>/", hotfix_delete_view, name="hotfix_delete"),
]
