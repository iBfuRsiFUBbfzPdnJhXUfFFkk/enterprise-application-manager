from django.http import HttpRequest, HttpResponse

from core.models.login_credential import LoginCredential
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def login_credential_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        login_credential = LoginCredential.objects.get(id=model_id)
        historical_records = login_credential.history.all()
    except LoginCredential.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/login_credential/login_credential_detail.html',
        context={
            'login_credential': login_credential,
            'historical_records': historical_records,
        }
    )
