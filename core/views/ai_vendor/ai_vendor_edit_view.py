from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.ai_vendor_form import AIVendorForm
from core.models.ai_vendor import AIVendor
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def ai_vendor_edit_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        ai_vendor = AIVendor.objects.get(id=model_id)
    except AIVendor.DoesNotExist:
        return generic_500(request=request)

    if request.method == 'POST':
        form = AIVendorForm(request.POST, instance=ai_vendor)
        if form.is_valid():
            form.save()
            return redirect('ai_vendor')
    else:
        form = AIVendorForm(instance=ai_vendor)

    return base_render(
        request=request,
        template_name='authenticated/ai_vendor/ai_vendor_form.html',
        context={'form': form}
    )
