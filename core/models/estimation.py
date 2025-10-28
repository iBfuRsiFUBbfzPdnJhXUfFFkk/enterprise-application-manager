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

    def get_total_hours_junior(self):
        """Calculate total junior developer hours from all items."""
        return sum(item.hours_junior or 0 for item in self.items.all())

    def get_total_hours_mid(self):
        """Calculate total mid-level developer hours from all items."""
        return sum(item.hours_mid or 0 for item in self.items.all())

    def get_total_hours_senior(self):
        """Calculate total senior developer hours from all items."""
        return sum(item.hours_senior or 0 for item in self.items.all())

    def get_total_hours_lead(self):
        """Calculate total lead developer hours from all items."""
        return sum(item.hours_lead or 0 for item in self.items.all())

    def get_total_hours_all_levels(self):
        """Calculate total hours across all developer levels."""
        return (
            self.get_total_hours_junior() +
            self.get_total_hours_mid() +
            self.get_total_hours_senior() +
            self.get_total_hours_lead()
        )

    def get_contingency_hours(self):
        """Calculate contingency hours based on padding percentage."""
        total = self.get_total_hours_all_levels()
        return total * (self.contingency_padding_percent / 100)

    def get_grand_total_hours(self):
        """Calculate grand total including contingency padding."""
        return self.get_total_hours_all_levels() + self.get_contingency_hours()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['-id']
        verbose_name = 'Estimation'
        verbose_name_plural = 'Estimations'
