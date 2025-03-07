from django.db.models import Model

from core.models.common.field_factories.create_generic_uuid import create_generic_uuid


class AbstractEnumerationAttackUuid(Model):
    enumeration_attack_uuid: str | None = create_generic_uuid()

    class Meta:
        abstract = True
