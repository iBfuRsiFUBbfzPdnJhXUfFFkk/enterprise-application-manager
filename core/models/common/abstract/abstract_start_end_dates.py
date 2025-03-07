from datetime import date

from django.db.models import Model

from core.models.common.field_factories.create_generic_date import create_generic_date


class AbstractStartEndDates(Model):
    date_end: date | None = create_generic_date()
    date_start: date | None = create_generic_date()

    class Meta:
        abstract = True
