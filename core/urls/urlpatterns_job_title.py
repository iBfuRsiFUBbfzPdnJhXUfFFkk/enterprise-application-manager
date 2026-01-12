from django.urls import URLPattern, URLResolver, path

from core.views.job_title import (
    job_title_add_view,
    job_title_delete_view,
    job_title_detail_view,
    job_title_edit_view,
    job_title_view,
)

urlpatterns_job_title: list[URLPattern | URLResolver] = [
    path("job_title/", job_title_view, name="job_title"),
    path("job_title/edit/<int:model_id>/", job_title_edit_view, name="job_title_edit"),
    path("job_title/new/", job_title_add_view, name="job_title_new"),
    path("job_title/<int:model_id>/", job_title_detail_view, name="job_title_detail"),
    path("job_title/delete/<int:model_id>/", job_title_delete_view, name="job_title_delete"),
]
