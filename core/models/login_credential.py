from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.utilities.encryption import decrypt_secret, encrypt_secret


class LoginCredential(AbstractBaseModel, AbstractComment, AbstractName):
    """
    Store login credentials with encrypted passwords.
    Can be linked to servers, databases, applications, service providers, tools, and people.
    """

    username = create_generic_varchar()

    encrypted_password = create_generic_varchar()

    # Foreign key relationships
    server = create_generic_fk(to='Server', related_name='login_credentials')
    database = create_generic_fk(to='Database', related_name='login_credentials_database')
    application = create_generic_fk(to='Application', related_name='login_credentials_application')
    service_provider = create_generic_fk(to='ServiceProvider', related_name='login_credentials_service_provider')
    tool = create_generic_fk(to='Tool', related_name='login_credentials_tool')
    person = create_generic_fk(to='Person', related_name='login_credentials_person')

    def set_encrypted_password(self, password: str | None) -> None:
        """Encrypt and store the password."""
        self.encrypted_password = encrypt_secret(secret=password)

    def get_decrypted_password(self) -> str | None:
        """Decrypt and return the password."""
        return decrypt_secret(encrypted_secret=self.encrypted_password)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
        verbose_name = 'Login Credential'
        verbose_name_plural = 'Login Credentials'
