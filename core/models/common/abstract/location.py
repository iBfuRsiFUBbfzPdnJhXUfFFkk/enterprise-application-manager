from django.db.models import Model

from core.models.common.enums.us_state_choices import US_STATE_CHOICES
from core.models.common.field_factories.create_generic_decimal import create_generic_decimal
from core.models.common.field_factories.create_generic_enum import create_generic_enum
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class Location(Model):
    location_address = create_generic_varchar()
    location_address_continued = create_generic_varchar()
    location_city = create_generic_varchar()
    location_county = create_generic_varchar()
    location_latitude = create_generic_decimal()
    location_longitude = create_generic_decimal()
    location_postal_code = create_generic_varchar()
    location_state_code = create_generic_enum(choices=US_STATE_CHOICES)

    class Meta:
        abstract = True
