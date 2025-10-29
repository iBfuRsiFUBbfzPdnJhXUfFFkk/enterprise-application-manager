from django.db import models
from django_generic_model_fields.create_generic_decimal import create_generic_decimal
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.models.application import Application
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.project import Project


class Estimation(AbstractBaseModel, AbstractComment, AbstractName):
    """
    Project/task estimation that can be tied to an Application and/or Project.
    Includes contingency padding for the overall estimation.
    """

    # Related entities
    application = create_generic_fk(
        to=Application,
        related_name='estimations'
    )
    project = create_generic_fk(
        to=Project,
        related_name='estimations'
    )

    # Estimation details
    description = create_generic_varchar()

    # Contingency padding as a percentage (e.g., 20 for 20%)
    contingency_padding_percent = create_generic_decimal()

    # Base hours (before uncertainty) - kept for reference
    def get_base_hours_junior(self):
        """Calculate total base junior developer hours from all items (before uncertainty)."""
        return sum(item.hours_junior or 0 for item in self.items.all())

    def get_base_hours_mid(self):
        """Calculate total base mid-level developer hours from all items (before uncertainty)."""
        return sum(item.hours_mid or 0 for item in self.items.all())

    def get_base_hours_senior(self):
        """Calculate total base senior developer hours from all items (before uncertainty)."""
        return sum(item.hours_senior or 0 for item in self.items.all())

    def get_base_hours_lead(self):
        """Calculate total base lead developer hours from all items (before uncertainty)."""
        return sum(item.hours_lead or 0 for item in self.items.all())

    # Hours with uncertainty applied per level
    def get_total_hours_junior_with_uncertainty(self):
        """Calculate total junior developer hours from all items with uncertainty applied."""
        return sum(item.get_junior_hours_with_uncertainty() for item in self.items.all())

    def get_total_hours_mid_with_uncertainty(self):
        """Calculate total mid-level developer hours from all items with uncertainty applied."""
        return sum(item.get_mid_hours_with_uncertainty() for item in self.items.all())

    def get_total_hours_senior_with_uncertainty(self):
        """Calculate total senior developer hours from all items with uncertainty applied."""
        return sum(item.get_senior_hours_with_uncertainty() for item in self.items.all())

    def get_total_hours_lead_with_uncertainty(self):
        """Calculate total lead developer hours from all items with uncertainty applied."""
        return sum(item.get_lead_hours_with_uncertainty() for item in self.items.all())

    def get_total_reviewer_hours(self):
        """Calculate total reviewer hours from all items (no uncertainty applied)."""
        return sum(item.get_reviewer_hours() for item in self.items.all())

    # Contingency padding per level
    def get_contingency_hours_junior(self):
        """Calculate contingency hours for junior level."""
        return self.get_total_hours_junior_with_uncertainty() * (self.contingency_padding_percent / 100)

    def get_contingency_hours_mid(self):
        """Calculate contingency hours for mid level."""
        return self.get_total_hours_mid_with_uncertainty() * (self.contingency_padding_percent / 100)

    def get_contingency_hours_senior(self):
        """Calculate contingency hours for senior level."""
        return self.get_total_hours_senior_with_uncertainty() * (self.contingency_padding_percent / 100)

    def get_contingency_hours_lead(self):
        """Calculate contingency hours for lead level."""
        return self.get_total_hours_lead_with_uncertainty() * (self.contingency_padding_percent / 100)

    def get_contingency_hours_reviewer(self):
        """Calculate contingency hours for reviewer."""
        return self.get_total_reviewer_hours() * (self.contingency_padding_percent / 100)

    # Grand totals per level (with uncertainty + contingency)
    def get_grand_total_hours_junior(self):
        """Calculate grand total junior hours (with uncertainty and contingency)."""
        return self.get_total_hours_junior_with_uncertainty() + self.get_contingency_hours_junior()

    def get_grand_total_hours_mid(self):
        """Calculate grand total mid-level hours (with uncertainty and contingency)."""
        return self.get_total_hours_mid_with_uncertainty() + self.get_contingency_hours_mid()

    def get_grand_total_hours_senior(self):
        """Calculate grand total senior hours (with uncertainty and contingency)."""
        return self.get_total_hours_senior_with_uncertainty() + self.get_contingency_hours_senior()

    def get_grand_total_hours_lead(self):
        """Calculate grand total lead hours (with uncertainty and contingency)."""
        return self.get_total_hours_lead_with_uncertainty() + self.get_contingency_hours_lead()

    def get_grand_total_reviewer_hours(self):
        """Calculate grand total reviewer hours (with contingency but no uncertainty)."""
        return self.get_total_reviewer_hours() + self.get_contingency_hours_reviewer()

    # Average across levels (optional aggregate view)
    def get_average_hours_with_uncertainty(self):
        """
        Calculate average hours across all developer levels with uncertainty applied.
        This is an optional aggregate view since hours per level are alternatives, not additive.
        """
        return sum(item.get_average_hours_with_uncertainty() for item in self.items.all())

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['-id']
        verbose_name = 'Estimation'
        verbose_name_plural = 'Estimations'
