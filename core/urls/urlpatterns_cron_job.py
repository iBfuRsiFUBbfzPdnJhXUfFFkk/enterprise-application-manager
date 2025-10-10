from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.cron_job import (
    cron_job_add_view,
    cron_job_delete_view,
    cron_job_detail_view,
    cron_job_edit_view,
    cron_job_view,
)

urlpatterns_cron_job: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='cron_job',
    view=cron_job_view,
    view_edit=cron_job_edit_view,
    view_new=cron_job_add_view,
)

# Add detail view
urlpatterns_cron_job.append(
    path(name='cron_job_detail', route='cron_job/<int:model_id>/', view=cron_job_detail_view)
)

# Add delete view
urlpatterns_cron_job.append(
    path(name='cron_job_delete', route='cron_job/delete/<int:model_id>/', view=cron_job_delete_view)
)
