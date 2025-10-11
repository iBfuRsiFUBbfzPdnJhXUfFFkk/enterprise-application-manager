from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.models.software_bill_of_material import SoftwareBillOfMaterial
from core.views.generic.generic_500 import generic_500


def software_bill_of_material_delete_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        software_bill_of_material = SoftwareBillOfMaterial.objects.get(id=model_id)
        software_bill_of_material.delete()
    except SoftwareBillOfMaterial.DoesNotExist:
        return generic_500(request=request)

    return redirect('software_bill_of_material')
