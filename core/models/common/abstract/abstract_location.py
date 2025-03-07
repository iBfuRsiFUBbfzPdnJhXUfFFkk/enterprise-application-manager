from django.db.models import Model

from core.models.common.enums.us_state_choices import US_STATE_CHOICES
from core.models.common.field_factories.create_generic_decimal import create_generic_decimal
from core.models.common.field_factories.create_generic_enum import create_generic_enum
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class AbstractLocation(Model):
    location_address: str | None = create_generic_varchar()
    location_address_continued: str | None = create_generic_varchar()
    location_city: str | None = create_generic_varchar()
    location_county: str | None = create_generic_varchar()
    location_latitude: float | None = create_generic_decimal()
    location_longitude: float | None = create_generic_decimal()
    location_postal_code: str | None = create_generic_varchar()
    location_state_code: str | None = create_generic_enum(choices=US_STATE_CHOICES)

    class Meta:
        abstract = True
