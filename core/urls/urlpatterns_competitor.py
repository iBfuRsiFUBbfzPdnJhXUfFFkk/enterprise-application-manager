from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.competitor import (
    competitor_add_view,
    competitor_delete_view,
    competitor_detail_view,
    competitor_edit_view,
    competitor_view,
)

urlpatterns_competitor: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='competitor',
    view=competitor_view,
    view_edit=competitor_edit_view,
    view_new=competitor_add_view,
)

# Add detail view
urlpatterns_competitor.append(
    path(name='competitor_detail', route='competitor/<int:model_id>/', view=competitor_detail_view)
)

# Add delete view
urlpatterns_competitor.append(
    path(name='competitor_delete', route='competitor/delete/<int:model_id>/', view=competitor_delete_view)
)
