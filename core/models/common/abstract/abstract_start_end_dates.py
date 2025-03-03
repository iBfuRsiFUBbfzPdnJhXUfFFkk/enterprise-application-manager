from django.db.models import Model

from core.models.common.field_factories.create_generic_date import create_generic_date


class AbstractStartEndDates(Model):
    date_end = create_generic_date()
    date_start = create_generic_date()

    class Meta:
        abstract = True