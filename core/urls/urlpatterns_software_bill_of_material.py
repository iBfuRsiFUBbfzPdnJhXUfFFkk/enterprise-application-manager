from django.urls import URLPattern, URLResolver, path

from core.views.software_bill_of_material import (
    software_bill_of_material_add_view,
    software_bill_of_material_delete_view,
    software_bill_of_material_detail_view,
    software_bill_of_material_edit_view,
    software_bill_of_material_view,
)

urlpatterns_software_bill_of_material: list[URLPattern | URLResolver] = [
    path("software_bill_of_material/", software_bill_of_material_view, name="software_bill_of_material"),
    path("software_bill_of_material/edit/<int:model_id>/", software_bill_of_material_edit_view, name="software_bill_of_material_edit"),
    path("software_bill_of_material/new/", software_bill_of_material_add_view, name="software_bill_of_material_new"),
    path("software_bill_of_material/<int:model_id>/", software_bill_of_material_detail_view, name="software_bill_of_material_detail"),
    path("software_bill_of_material/delete/<int:model_id>/", software_bill_of_material_delete_view, name="software_bill_of_material_delete"),
]
