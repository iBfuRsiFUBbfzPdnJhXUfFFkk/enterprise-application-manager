from django.http import HttpRequest, HttpResponse

from core.models.software_bill_of_material import SoftwareBillOfMaterial
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def software_bill_of_material_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        software_bill_of_material = SoftwareBillOfMaterial.objects.get(id=model_id)
        historical_records = software_bill_of_material.history.all()
    except SoftwareBillOfMaterial.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/software_bill_of_material/software_bill_of_material_detail.html',
        context={
            'software_bill_of_material': software_bill_of_material,
            'historical_records': historical_records,
        }
    )
