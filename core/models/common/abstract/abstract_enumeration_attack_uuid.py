from typing import Optional

from django.db.models import Model

from django_generic_model_fields.create_generic_uuid import create_generic_uuid


class AbstractEnumerationAttackUuid(Model):
    enumeration_attack_uuid: str | None = create_generic_uuid()

    @property
    def uuid(self) -> str | None:
        return self.enumeration_attack_uuid

    @classmethod
    def from_uuid(cls, uuid: str) -> Optional['AbstractEnumerationAttackUuid']:
        return cls.objects.filter(enumeration_attack_uuid=uuid).first()

    class Meta:
        abstract = True
