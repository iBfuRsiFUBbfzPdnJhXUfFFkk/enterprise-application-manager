from decimal import Decimal

from django_generic_model_fields.create_generic_decimal import create_generic_decimal
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_text import create_generic_text
from django_generic_model_fields.create_generic_enum import create_generic_enum

from core.models.common.abstract.abstract_base_model import AbstractBaseModel


class EstimationItem(AbstractBaseModel):
    """
    Individual line item within an estimation with hours for different developer levels.
    Includes cone of uncertainty, complexity level, and priority.
    The cone of uncertainty automatically determines the uncertainty padding multiplier.
    """

    # Cone of Uncertainty choices based on project phase
    CONE_OF_UNCERTAINTY_CHOICES = [
        ('INITIAL_CONCEPT', 'Initial Concept (4x uncertainty)'),
        ('APPROVED_PRODUCT', 'Approved Product Definition (2x uncertainty)'),
        ('REQUIREMENTS_COMPLETE', 'Requirements Complete (1.5x uncertainty)'),
        ('DESIGN_COMPLETE', 'Design Complete (1.25x uncertainty)'),
        ('IMPLEMENTATION_COMPLETE', 'Implementation Complete (1.1x uncertainty)'),
    ]

    # Cone of Uncertainty multipliers
    CONE_OF_UNCERTAINTY_MULTIPLIERS = {
        'INITIAL_CONCEPT': Decimal('4.0'),
        'APPROVED_PRODUCT': Decimal('2.0'),
        'REQUIREMENTS_COMPLETE': Decimal('1.5'),
        'DESIGN_COMPLETE': Decimal('1.25'),
        'IMPLEMENTATION_COMPLETE': Decimal('1.1'),
    }

    # Complexity level choices
    COMPLEXITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('VERY_HIGH', 'Very High'),
    ]

    # Priority choices
    PRIORITY_CHOICES = [
        ('CRITICAL', 'Critical'),
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]

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

    # Cone of Uncertainty - project phase indicator
    cone_of_uncertainty = create_generic_enum(
        choices=CONE_OF_UNCERTAINTY_CHOICES
    )

    # Complexity level
    complexity_level = create_generic_enum(
        choices=COMPLEXITY_CHOICES
    )

    # Priority
    priority = create_generic_enum(
        choices=PRIORITY_CHOICES
    )

    def get_uncertainty_multiplier(self):
        """Get the uncertainty multiplier based on the cone of uncertainty phase."""
        if self.cone_of_uncertainty:
            return self.CONE_OF_UNCERTAINTY_MULTIPLIERS.get(self.cone_of_uncertainty, Decimal('1.0'))
        return Decimal('1.0')

    # Individual level hours with uncertainty applied
    def get_junior_hours_with_uncertainty(self):
        """Calculate junior hours including uncertainty padding."""
        return (self.hours_junior or 0) * self.get_uncertainty_multiplier()

    def get_mid_hours_with_uncertainty(self):
        """Calculate mid-level hours including uncertainty padding."""
        return (self.hours_mid or 0) * self.get_uncertainty_multiplier()

    def get_senior_hours_with_uncertainty(self):
        """Calculate senior hours including uncertainty padding."""
        return (self.hours_senior or 0) * self.get_uncertainty_multiplier()

    def get_lead_hours_with_uncertainty(self):
        """Calculate lead hours including uncertainty padding."""
        return (self.hours_lead or 0) * self.get_uncertainty_multiplier()

    def get_average_hours_with_uncertainty(self):
        """
        Calculate average hours across all developer levels with uncertainty applied.
        This is an optional aggregate view since hours per level are alternatives, not additive.
        """
        total = (
            self.get_junior_hours_with_uncertainty() +
            self.get_mid_hours_with_uncertainty() +
            self.get_senior_hours_with_uncertainty() +
            self.get_lead_hours_with_uncertainty()
        )
        # Count non-zero hours to get accurate average
        count = sum([
            1 if self.hours_junior else 0,
            1 if self.hours_mid else 0,
            1 if self.hours_senior else 0,
            1 if self.hours_lead else 0,
        ])
        return total / count if count > 0 else Decimal('0')

    def __str__(self):
        return f"{self.description[:50]}..." if len(self.description) > 50 else self.description

    class Meta:
        ordering = ['id']
        verbose_name = 'Estimation Item'
        verbose_name_plural = 'Estimation Items'
