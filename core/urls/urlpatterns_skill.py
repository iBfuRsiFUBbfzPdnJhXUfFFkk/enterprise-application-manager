from django.urls import URLPattern, URLResolver, path

from core.views.skill import (
    skill_add_view,
    skill_delete_view,
    skill_detail_view,
    skill_edit_view,
    skill_view,
)

urlpatterns_skill: list[URLPattern | URLResolver] = [
    path("skill/", skill_view, name="skill"),
    path("skill/edit/<int:model_id>/", skill_edit_view, name="skill_edit"),
    path("skill/new/", skill_add_view, name="skill_new"),
    path("skill/<int:model_id>/", skill_detail_view, name="skill_detail"),
    path("skill/delete/<int:model_id>/", skill_delete_view, name="skill_delete"),
]
