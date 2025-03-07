from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar
from core.utilities.encryption import encrypt_secret, decrypt_secret


class Secret(AbstractBaseModel, AbstractComment, AbstractName):
    encrypted_value = create_generic_varchar()

    def set_encrypted_value(self, secret: str | None) -> None:
        self.encrypted_value = encrypt_secret(secret=secret)

    def get_encrypted_value(self) -> str | None:
        return decrypt_secret(encrypted_secret=self.encrypted_value)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
