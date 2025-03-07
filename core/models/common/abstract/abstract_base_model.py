from django.db.models import Model
from simple_history.models import HistoricalRecords

from core.models.common.field_factories.create_generic_uuid import create_generic_uuid


class AbstractBaseModel(Model):
    enumeration_attack_uuid: str | None = create_generic_uuid()
    history: HistoricalRecords = None

    class Meta:
        abstract = True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.history = HistoricalRecords(
            inherit=True,
            verbose_name=f"_Historical Record for {cls.__name__}",
            verbose_name_plural=f"_Historical Records for {cls.__name__}",
        )
        cls.add_to_class(name='history', value=cls.history)
