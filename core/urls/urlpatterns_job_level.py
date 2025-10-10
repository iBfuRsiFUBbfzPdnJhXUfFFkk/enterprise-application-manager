from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.job_level import (
    job_level_add_view,
    job_level_delete_view,
    job_level_detail_view,
    job_level_edit_view,
    job_level_view,
)

urlpatterns_job_level: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='job_level',
    view=job_level_view,
    view_edit=job_level_edit_view,
    view_new=job_level_add_view,
)

# Add detail view
urlpatterns_job_level.append(
    path(name='job_level_detail', route='job_level/<int:model_id>/', view=job_level_detail_view)
)

# Add delete view
urlpatterns_job_level.append(
    path(name='job_level_delete', route='job_level/delete/<int:model_id>/', view=job_level_delete_view)
)
