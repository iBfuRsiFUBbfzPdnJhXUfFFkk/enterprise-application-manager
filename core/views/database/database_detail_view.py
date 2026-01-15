import logging

from django.http import HttpRequest, HttpResponse

from core.models.database import Database
from core.utilities.base_render import base_render
from core.utilities.encryption import InvalidEncryptionKeyError
from core.views.generic.generic_500 import generic_500

logger = logging.getLogger(__name__)


def database_detail_view(request: HttpRequest, model_id: int) -> HttpResponse:
    try:
        database = Database.objects.get(id=model_id)
        historical_records = list(database.history.all())
        created_record = historical_records[-1] if historical_records else None
        updated_record = historical_records[0] if historical_records else None
    except Database.DoesNotExist:
        return generic_500(request=request)

    # Try to decrypt all fields, collect errors
    decryption_errors = []

    def safe_decrypt(func, field_name):
        """Helper to safely decrypt and collect errors."""
        try:
            return func()
        except InvalidEncryptionKeyError as e:
            decryption_errors.append(f"{field_name}: {str(e)}")
            logger.error(f"Failed to decrypt Database id={database.id} {field_name}: {e}")
            return None
        except Exception as e:
            decryption_errors.append(f"{field_name}: Unexpected error")
            logger.error(f"Unexpected error decrypting Database id={database.id} {field_name}: {e}")
            return None

    decrypted_username = safe_decrypt(database.get_encrypted_username, "username")
    decrypted_password = safe_decrypt(database.get_encrypted_password, "password")
    decrypted_ssh_tunnel_username = safe_decrypt(database.get_encrypted_ssh_tunnel_username, "SSH username")
    decrypted_ssh_tunnel_password = safe_decrypt(database.get_encrypted_ssh_tunnel_password, "SSH password")

    # Connection string may also fail if credentials fail
    connection_string = None
    try:
        connection_string = database.get_connection_string()
    except Exception:
        pass  # Already captured credential errors

    return base_render(
        request=request,
        template_name='authenticated/database/database_detail.html',
        context={
            'database': database,
            'historical_records': historical_records,
            'created_record': created_record,
            'updated_record': updated_record,
            'decrypted_username': decrypted_username,
            'decrypted_password': decrypted_password,
            'decrypted_ssh_tunnel_username': decrypted_ssh_tunnel_username,
            'decrypted_ssh_tunnel_password': decrypted_ssh_tunnel_password,
            'connection_string': connection_string,
            'decryption_errors': decryption_errors,
        }
    )
