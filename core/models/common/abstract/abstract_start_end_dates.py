from datetime import date

from django.db import models


class AbstractStartEndDates(models.Model):
    date_end: date | None = models.DateField(null=True, blank=True)
    date_start: date | None = models.DateField(null=True, blank=True)

    @property
    def date_range_string(self) -> str:
        if self.date_start is not None and self.date_end is not None:
            return f"[{self.date_start} - {self.date_end}]"
        if self.date_start is not None:
            return f"[{self.date_start} - TBD]"
        if self.date_end is not None:
            return f"[TBD - {self.date_end}]"
        return "TBD"

    class Meta:
        abstract = True
