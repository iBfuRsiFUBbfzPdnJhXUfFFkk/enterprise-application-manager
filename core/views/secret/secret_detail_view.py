import logging

from django.http import HttpRequest, HttpResponse

from core.models.secret import Secret
from core.utilities.base_render import base_render
from core.utilities.encryption import InvalidEncryptionKeyError
from core.views.generic.generic_500 import generic_500

logger = logging.getLogger(__name__)


def secret_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        secret = Secret.objects.get(id=model_id)
        historical_records = list(secret.history.all())
        created_record = historical_records[-1] if historical_records else None
        updated_record = historical_records[0] if historical_records else None
    except Secret.DoesNotExist:
        return generic_500(request=request)

    # Try to decrypt value, handle errors gracefully
    decrypted_value = None
    decryption_error = None

    try:
        decrypted_value = secret.get_encrypted_value()
    except InvalidEncryptionKeyError as e:
        decryption_error = str(e)
        logger.error(f"Failed to decrypt Secret id={secret.id}: {e}")
    except Exception as e:
        decryption_error = "Unexpected error during decryption"
        logger.error(f"Unexpected error decrypting Secret id={secret.id}: {e}")

    return base_render(
        request=request,
        template_name='authenticated/secret/secret_detail.html',
        context={
            'secret': secret,
            'historical_records': historical_records,
            'created_record': created_record,
            'updated_record': updated_record,
            'decrypted_value': decrypted_value,
            'decryption_error': decryption_error,
        }
    )
