from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.software_bill_of_material import (
    software_bill_of_material_add_view,
    software_bill_of_material_delete_view,
    software_bill_of_material_detail_view,
    software_bill_of_material_edit_view,
    software_bill_of_material_view,
)

urlpatterns_software_bill_of_material: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='software_bill_of_material',
    view=software_bill_of_material_view,
    view_edit=software_bill_of_material_edit_view,
    view_new=software_bill_of_material_add_view,
)

# Add detail view
urlpatterns_software_bill_of_material.append(
    path(name='software_bill_of_material_detail', route='software_bill_of_material/<int:model_id>/', view=software_bill_of_material_detail_view)
)

# Add delete view
urlpatterns_software_bill_of_material.append(
    path(name='software_bill_of_material_delete', route='software_bill_of_material/delete/<int:model_id>/', view=software_bill_of_material_delete_view)
)
