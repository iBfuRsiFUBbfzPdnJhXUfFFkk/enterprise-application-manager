from django.urls import URLPattern, URLResolver, path

from core.views.team import (
    team_add_view,
    team_delete_view,
    team_detail_view,
    team_edit_view,
    team_view,
)

urlpatterns_team: list[URLPattern | URLResolver] = [
    path("team/", team_view, name="team"),
    path("team/edit/<int:model_id>/", team_edit_view, name="team_edit"),
    path("team/new/", team_add_view, name="team_new"),
    path("team/<int:model_id>/", team_detail_view, name="team_detail"),
    path("team/delete/<int:model_id>/", team_delete_view, name="team_delete"),
]
