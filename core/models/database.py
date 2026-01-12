from django.db import models
from core.models.application import Application
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_version import AbstractVersion
from core.models.common.enums.data_storage_form_choices import DATA_STORAGE_FORM_CHOICES
from core.models.common.enums.database_flavor_choices import DATABASE_FLAVOR_CHOICES
from core.models.common.enums.environment_choices import ENVIRONMENT_CHOICES
from core.utilities.encryption import encrypt_secret, decrypt_secret


class Database(AbstractBaseModel, AbstractComment, AbstractVersion):
    application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True, blank=True, related_name='databases')
    encrypted_password = models.CharField(max_length=255, null=True, blank=True)
    encrypted_username = models.CharField(max_length=255, null=True, blank=True)
    hostname = models.CharField(max_length=255, null=True, blank=True)
    ip_v4_internal = models.CharField(max_length=255, null=True, blank=True)
    port = models.IntegerField(null=True, blank=True)
    schema = models.CharField(max_length=255, null=True, blank=True)
    type_data_storage_form = models.CharField(max_length=255, choices=DATA_STORAGE_FORM_CHOICES, null=True, blank=True)
    type_database_flavor = models.CharField(max_length=255, choices=DATABASE_FLAVOR_CHOICES, null=True, blank=True)
    type_environment = models.CharField(max_length=255, choices=ENVIRONMENT_CHOICES, null=True, blank=True)

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
