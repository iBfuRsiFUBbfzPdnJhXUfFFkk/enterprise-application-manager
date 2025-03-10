from django.db.models import Model

from django_generic_model_fields.create_generic_integer import create_generic_integer
from core.utilities.coerce_integer import coerce_integer


class AbstractScrumCapacityBase(Model):
    scrum_capacity_base: int | None = create_generic_integer()

    @property
    def coerced_scrum_capacity_base_local(self) -> int:
        return coerce_integer(self.scrum_capacity_base)

    class Meta:
        abstract = True
