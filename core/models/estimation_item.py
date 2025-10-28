from django_generic_model_fields.create_generic_decimal import create_generic_decimal
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_text import create_generic_text

from core.models.common.abstract.abstract_base_model import AbstractBaseModel


class EstimationItem(AbstractBaseModel):
    """
    Individual line item within an estimation with hours for different developer levels.
    """

    # Link to parent estimation
    estimation = create_generic_fk(
        to='Estimation',
        related_name='items'
    )

    # Item details
    description = create_generic_text()

    # Hours by developer level
    hours_junior = create_generic_decimal()
    hours_mid = create_generic_decimal()
    hours_senior = create_generic_decimal()
    hours_lead = create_generic_decimal()

    def get_total_hours(self):
        """Calculate total hours for this item across all developer levels."""
        return (
            (self.hours_junior or 0) +
            (self.hours_mid or 0) +
            (self.hours_senior or 0) +
            (self.hours_lead or 0)
        )

    def __str__(self):
        return f"{self.description[:50]}..." if len(self.description) > 50 else self.description

    class Meta:
        ordering = ['id']
        verbose_name = 'Estimation Item'
        verbose_name_plural = 'Estimation Items'
