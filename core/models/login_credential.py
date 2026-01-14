
from django.db import models
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.utilities.encryption import decrypt_secret, encrypt_secret

class LoginCredential(AbstractBaseModel, AbstractComment, AbstractName):
    """
    Store login credentials with encrypted passwords.
    Can be linked to servers, databases, applications, service providers, tools, and people.
    """

    username = models.CharField(max_length=255, null=True, blank=True)

    encrypted_password = models.CharField(max_length=255, null=True, blank=True)

    # Foreign key relationships
    server = models.ForeignKey('Server', on_delete=models.SET_NULL, null=True, blank=True, related_name='login_credentials')
    database = models.ForeignKey('Database', on_delete=models.SET_NULL, null=True, blank=True, related_name='login_credentials_database')
    application = models.ForeignKey('Application', on_delete=models.SET_NULL, null=True, blank=True, related_name='login_credentials_application')
    service_provider = models.ForeignKey('ServiceProvider', on_delete=models.SET_NULL, null=True, blank=True, related_name='login_credentials_service_provider')
    tool = models.ForeignKey('Tool', on_delete=models.SET_NULL, null=True, blank=True, related_name='login_credentials_tool')
    person = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='login_credentials_person')

    def set_encrypted_password(self, password: str | None) -> None:
        """
        Encrypt and store the password.
        Empty strings are treated as None and will not be encrypted.
        """
        # Treat empty strings as None
        if password == "" or (isinstance(password, str) and password.strip() == ""):
            self.encrypted_password = None
        else:
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
