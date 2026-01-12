from django.db import models

from core.models.common.enums.us_state_choices import US_STATE_CHOICES


class AbstractLocation(models.Model):
    location_address: str | None = models.CharField(max_length=255, null=True, blank=True)
    location_address_continued: str | None = models.CharField(max_length=255, null=True, blank=True)
    location_city: str | None = models.CharField(max_length=255, null=True, blank=True)
    location_county: str | None = models.CharField(max_length=255, null=True, blank=True)
    location_latitude: float | None = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_longitude: float | None = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_postal_code: str | None = models.CharField(max_length=255, null=True, blank=True)
    location_state_code: str | None = models.CharField(max_length=255, choices=US_STATE_CHOICES, null=True, blank=True)

    class Meta:
        abstract = True
