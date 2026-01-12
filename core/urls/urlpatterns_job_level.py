from django.urls import URLPattern, URLResolver, path

from core.views.job_level import (
    job_level_add_view,
    job_level_delete_view,
    job_level_detail_view,
    job_level_edit_view,
    job_level_view,
)

urlpatterns_job_level: list[URLPattern | URLResolver] = [
    path("job_level/", job_level_view, name="job_level"),
    path("job_level/edit/<int:model_id>/", job_level_edit_view, name="job_level_edit"),
    path("job_level/new/", job_level_add_view, name="job_level_new"),
    path("job_level/<int:model_id>/", job_level_detail_view, name="job_level_detail"),
    path("job_level/delete/<int:model_id>/", job_level_delete_view, name="job_level_delete"),
]
