from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.job_title import (
    job_title_add_view,
    job_title_delete_view,
    job_title_detail_view,
    job_title_edit_view,
    job_title_view,
)

urlpatterns_job_title: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='job_title',
    view=job_title_view,
    view_edit=job_title_edit_view,
    view_new=job_title_add_view,
)

# Add detail view
urlpatterns_job_title.append(
    path(name='job_title_detail', route='job_title/<int:model_id>/', view=job_title_detail_view)
)

# Add delete view
urlpatterns_job_title.append(
    path(name='job_title_delete', route='job_title/delete/<int:model_id>/', view=job_title_delete_view)
)
