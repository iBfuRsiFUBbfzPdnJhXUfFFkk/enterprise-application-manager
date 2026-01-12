from django.db import models

from core.utilities.coerce_integer import coerce_integer


class AbstractScrumCapacityBase(models.Model):
    scrum_capacity_base: int | None = models.IntegerField(null=True, blank=True)

    @property
    def coerced_scrum_capacity_base_local(self) -> int:
        return coerce_integer(self.scrum_capacity_base)

    class Meta:
        abstract = True
