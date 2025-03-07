from datetime import date

from django.db.models import Model

from core.models.common.field_factories.create_generic_date import create_generic_date


class AbstractStartEndDates(Model):
    date_end: date | None = create_generic_date()
    date_start: date | None = create_generic_date()

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
