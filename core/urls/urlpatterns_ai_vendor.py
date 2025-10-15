from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.ai_vendor import (
    ai_vendor_add_view,
    ai_vendor_delete_view,
    ai_vendor_detail_view,
    ai_vendor_edit_view,
    ai_vendor_view,
)

urlpatterns_ai_vendor: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='ai_vendor',
    view=ai_vendor_view,
    view_edit=ai_vendor_edit_view,
    view_new=ai_vendor_add_view,
)

# Add detail view
urlpatterns_ai_vendor.append(
    path(name='ai_vendor_detail', route='ai-vendor/<int:model_id>/', view=ai_vendor_detail_view)
)

# Add delete view
urlpatterns_ai_vendor.append(
    path(name='ai_vendor_delete', route='ai-vendor/delete/<int:model_id>/', view=ai_vendor_delete_view)
)
