from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.ai_governance import (
    ai_governance_add_view,
    ai_governance_delete_view,
    ai_governance_detail_view,
    ai_governance_edit_view,
    ai_governance_view,
)

urlpatterns_ai_governance: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='ai_governance',
    view=ai_governance_view,
    view_edit=ai_governance_edit_view,
    view_new=ai_governance_add_view,
)

# Add detail view
urlpatterns_ai_governance.append(
    path(name='ai_governance_detail', route='ai-governance/<int:model_id>/', view=ai_governance_detail_view)
)

# Add delete view
urlpatterns_ai_governance.append(
    path(name='ai_governance_delete', route='ai-governance/delete/<int:model_id>/', view=ai_governance_delete_view)
)
