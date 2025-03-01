from django.db.models import Model
from simple_history.models import HistoricalRecords

from core.models.common.field_factories.create_generic_uuid import create_generic_uuid


class BaseModel(Model):
    enumeration_attack_uuid = create_generic_uuid()
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
