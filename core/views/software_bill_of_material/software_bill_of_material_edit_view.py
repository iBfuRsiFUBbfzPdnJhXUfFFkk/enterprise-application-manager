from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.software_bill_of_material_form import SoftwareBillOfMaterialForm
from core.models.software_bill_of_material import SoftwareBillOfMaterial
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def software_bill_of_material_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        software_bill_of_material = SoftwareBillOfMaterial.objects.get(id=model_id)
    except SoftwareBillOfMaterial.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = SoftwareBillOfMaterialForm(request.POST, instance=software_bill_of_material)
        if form.is_valid():
            form.save()
            return redirect('software_bill_of_material')
    else:
        form = SoftwareBillOfMaterialForm(instance=software_bill_of_material)

    return base_render(
        request=request,
        template_name='authenticated/software_bill_of_material/software_bill_of_material_form.html',
        context={'form': form}
    )
