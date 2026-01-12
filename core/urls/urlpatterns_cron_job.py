from django.urls import URLPattern, URLResolver, path

from core.views.cron_job import (
    cron_job_add_view,
    cron_job_delete_view,
    cron_job_detail_view,
    cron_job_edit_view,
    cron_job_view,
)

urlpatterns_cron_job: list[URLPattern | URLResolver] = [
    path("cron_job/", cron_job_view, name="cron_job"),
    path("cron_job/edit/<int:model_id>/", cron_job_edit_view, name="cron_job_edit"),
    path("cron_job/new/", cron_job_add_view, name="cron_job_new"),
    path("cron_job/<int:model_id>/", cron_job_detail_view, name="cron_job_detail"),
    path("cron_job/delete/<int:model_id>/", cron_job_delete_view, name="cron_job_delete"),
]
