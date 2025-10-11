from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.software_bill_of_material_form import SoftwareBillOfMaterialForm
from core.utilities.base_render import base_render


def software_bill_of_material_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = SoftwareBillOfMaterialForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('software_bill_of_material')
    else:
        form = SoftwareBillOfMaterialForm()

    return base_render(
        request=request,
        template_name='authenticated/software_bill_of_material/software_bill_of_material_form.html',
        context={'form': form}
    )
