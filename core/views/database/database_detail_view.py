from django.http import HttpRequest, HttpResponse

from core.models.database import Database
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def database_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        database = Database.objects.get(id=model_id)
        historical_records = database.history.all()
    except Database.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/database/database_detail.html',
        context={
            'database': database,
            'historical_records': historical_records,
            'decrypted_username': database.get_encrypted_username(),
            'decrypted_password': database.get_encrypted_password(),
        }
    )
