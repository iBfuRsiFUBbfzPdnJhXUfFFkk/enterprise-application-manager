from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.ai_hallucination import (
    ai_hallucination_add_view,
    ai_hallucination_delete_view,
    ai_hallucination_detail_view,
    ai_hallucination_edit_view,
    ai_hallucination_view,
)

urlpatterns_ai_hallucination: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='ai_hallucination',
    view=ai_hallucination_view,
    view_edit=ai_hallucination_edit_view,
    view_new=ai_hallucination_add_view,
)

# Add detail view
urlpatterns_ai_hallucination.append(
    path(name='ai_hallucination_detail', route='ai-hallucination/<int:model_id>/', view=ai_hallucination_detail_view)
)

# Add delete view
urlpatterns_ai_hallucination.append(
    path(name='ai_hallucination_delete', route='ai-hallucination/delete/<int:model_id>/', view=ai_hallucination_delete_view)
)
