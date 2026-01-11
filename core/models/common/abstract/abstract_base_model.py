from simple_history.models import HistoricalRecords

from core.models.common.abstract.abstract_enumeration_attack_uuid import AbstractEnumerationAttackUuid


class AbstractBaseModel(AbstractEnumerationAttackUuid):
    history: HistoricalRecords = None

    class Meta:
        abstract = True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # Check if this model should skip history tracking
        disable_history = getattr(cls, '_disable_history', False)

        if not disable_history:
            cls.history = HistoricalRecords(
                inherit=True,
                verbose_name=f"_Historical Record for {cls.__name__}",
                verbose_name_plural=f"_Historical Records for {cls.__name__}",
            )
            cls.add_to_class(name='history', value=cls.history)
        else:
            # Set history to None for models that opt-out
            cls.history = None
