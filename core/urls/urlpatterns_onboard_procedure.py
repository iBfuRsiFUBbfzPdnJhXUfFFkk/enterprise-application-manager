from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.onboard_procedure import (
    onboard_procedure_add_view,
    onboard_procedure_delete_view,
    onboard_procedure_detail_view,
    onboard_procedure_edit_view,
    onboard_procedure_view,
)

urlpatterns_onboard_procedure: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='onboard_procedure',
    view=onboard_procedure_view,
    view_edit=onboard_procedure_edit_view,
    view_new=onboard_procedure_add_view,
)

# Add detail view
urlpatterns_onboard_procedure.append(
    path(name='onboard_procedure_detail', route='onboard_procedure/<int:model_id>/', view=onboard_procedure_detail_view)
)

# Add delete view
urlpatterns_onboard_procedure.append(
    path(name='onboard_procedure_delete', route='onboard_procedure/delete/<int:model_id>/', view=onboard_procedure_delete_view)
)
