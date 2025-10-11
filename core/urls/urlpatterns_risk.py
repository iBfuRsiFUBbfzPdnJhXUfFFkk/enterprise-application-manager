from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.risk import (
    risk_add_view,
    risk_delete_view,
    risk_detail_view,
    risk_edit_view,
    risk_view,
)

urlpatterns_risk: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='risk',
    view=risk_view,
    view_edit=risk_edit_view,
    view_new=risk_add_view,
)

# Add detail view
urlpatterns_risk.append(
    path(name='risk_detail', route='risk/<int:model_id>/', view=risk_detail_view)
)

# Add delete view
urlpatterns_risk.append(
    path(name='risk_delete', route='risk/delete/<int:model_id>/', view=risk_delete_view)
)
