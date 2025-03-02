from core.models.application import Application
from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.version import Version
from core.models.common.enums.data_storage_form_choices import DATA_STORAGE_FORM_CHOICES
from core.models.common.enums.database_flavor_choices import DATABASE_FLAVOR_CHOICES
from core.models.common.enums.environment_choices import ENVIRONMENT_CHOICES
from core.models.common.field_factories.create_generic_enum import create_generic_enum
from core.models.common.field_factories.create_generic_fk import create_generic_fk
from core.models.common.field_factories.create_generic_integer import create_generic_integer
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar
from core.utilities.encryption import encrypt_secret, decrypt_secret


class Database(BaseModel, Comment, Version):
    application = create_generic_fk(related_name='databases', to=Application)
    encrypted_password = create_generic_varchar()
    encrypted_username = create_generic_varchar()
    hostname = create_generic_varchar()
    ip_v4_internal = create_generic_varchar()
    port = create_generic_integer()
    schema = create_generic_varchar()
    type_data_storage_form = create_generic_enum(choices=DATA_STORAGE_FORM_CHOICES)
    type_database_flavor = create_generic_enum(choices=DATABASE_FLAVOR_CHOICES)
    type_environment = create_generic_enum(choices=ENVIRONMENT_CHOICES)

    def set_encrypted_password(self, secret: str | None) -> None:
        self.encrypted_password = encrypt_secret(secret=secret)

    def get_encrypted_password(self) -> str | None:
        return decrypt_secret(encrypted_secret=self.encrypted_password)

    def set_encrypted_username(self, secret: str | None) -> None:
        self.encrypted_username = encrypt_secret(secret=secret)

    def get_encrypted_username(self) -> str | None:
        return decrypt_secret(encrypted_secret=self.encrypted_username)

    def __str__(self):
        return f"{self.application.acronym if self.application is not None else 'N/A'} - {self.type_environment} - v{self.version}"

    class Meta:
        ordering = ['schema', '-id']
