from django.db import models
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.utilities.encryption import encrypt_secret, decrypt_secret

class Secret(AbstractBaseModel, AbstractComment, AbstractName):
    encrypted_value = models.CharField(max_length=255, null=True, blank=True)

    def set_encrypted_value(self, secret: str | None) -> None:
        """
        Set and encrypt a secret value.
        Empty strings are treated as None and will not be encrypted.
        """
        # Treat empty strings as None
        if secret == "" or (isinstance(secret, str) and secret.strip() == ""):
            self.encrypted_value = None
        else:
            self.encrypted_value = encrypt_secret(secret=secret)

    def get_encrypted_value(self) -> str | None:
        return decrypt_secret(encrypted_secret=self.encrypted_value)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
