from typing import Optional

from django.db import models


class AbstractEnumerationAttackUuid(models.Model):
    enumeration_attack_uuid: str | None = models.UUIDField(null=True, blank=True)

    @property
    def uuid(self) -> str | None:
        return self.enumeration_attack_uuid

    @classmethod
    def from_uuid(cls, uuid: str) -> Optional['AbstractEnumerationAttackUuid']:
        return cls.objects.filter(enumeration_attack_uuid=uuid).first()

    class Meta:
        abstract = True
