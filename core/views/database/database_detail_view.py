from django.http import HttpRequest, HttpResponse

from core.models.database import Database
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def database_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        database = Database.objects.get(id=model_id)
        historical_records = list(database.history.all())
        created_record = historical_records[-1] if historical_records else None
        updated_record = historical_records[0] if historical_records else None
    except Database.DoesNotExist:
        return generic_500(request=request)

    return base_render(
        request=request,
        template_name='authenticated/database/database_detail.html',
        context={
            'database': database,
            'historical_records': historical_records,
            'created_record': created_record,
            'updated_record': updated_record,
            'decrypted_username': database.get_encrypted_username(),
            'decrypted_password': database.get_encrypted_password(),
        }
    )
