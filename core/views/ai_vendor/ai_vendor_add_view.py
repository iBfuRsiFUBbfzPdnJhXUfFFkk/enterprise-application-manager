from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

from core.forms.ai_vendor_form import AIVendorForm
from core.utilities.base_render import base_render


def ai_vendor_add_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = AIVendorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ai_vendor')
    else:
        form = AIVendorForm()

    return base_render(
        request=request,
        template_name='authenticated/ai_vendor/ai_vendor_form.html',
        context={'form': form}
    )
