from django.http import HttpRequest, HttpResponse

from core.models.software_bill_of_material import SoftwareBillOfMaterial
from core.views.generic.generic_view import generic_view


def software_bill_of_material_view(request: HttpRequest) -> HttpResponse:
    return generic_view(
        model_cls=SoftwareBillOfMaterial,
        name='software_bill_of_material',
        request=request,
    )
