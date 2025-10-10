from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.external_blocker import (
    external_blocker_add_view,
    external_blocker_delete_view,
    external_blocker_detail_view,
    external_blocker_edit_view,
    external_blocker_view,
)

urlpatterns_external_blocker: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='external_blocker',
    view=external_blocker_view,
    view_edit=external_blocker_edit_view,
    view_new=external_blocker_add_view,
)

# Add detail view
urlpatterns_external_blocker.append(
    path(name='external_blocker_detail', route='external_blocker/<int:model_id>/', view=external_blocker_detail_view)
)

# Add delete view
urlpatterns_external_blocker.append(
    path(name='external_blocker_delete', route='external_blocker/delete/<int:model_id>/', view=external_blocker_delete_view)
)
