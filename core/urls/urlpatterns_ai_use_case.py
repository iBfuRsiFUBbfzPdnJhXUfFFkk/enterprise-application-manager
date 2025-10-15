from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.ai_use_case import (
    ai_use_case_add_view,
    ai_use_case_delete_view,
    ai_use_case_detail_view,
    ai_use_case_edit_view,
    ai_use_case_view,
)

urlpatterns_ai_use_case: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='ai_use_case',
    view=ai_use_case_view,
    view_edit=ai_use_case_edit_view,
    view_new=ai_use_case_add_view,
)

# Add detail view
urlpatterns_ai_use_case.append(
    path(name='ai_use_case_detail', route='ai-use-case/<int:model_id>/', view=ai_use_case_detail_view)
)

# Add delete view
urlpatterns_ai_use_case.append(
    path(name='ai_use_case_delete', route='ai-use-case/delete/<int:model_id>/', view=ai_use_case_delete_view)
)
