from django.db import models

from core.models.application import Application
from core.models.common.abstract.abstract_acronym import AbstractAcronym
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_location import AbstractLocation
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.abstract.abstract_uniform_resource_locator import AbstractUniformResourceLocator
from core.models.common.enums.employee_count_tier_choices import EMPLOYEE_COUNT_TIER_CHOICES
from core.models.common.enums.revenue_tier_choices import REVENUE_TIER_CHOICES
from core.models.organization import Organization
from core.utilities.get_name_acronym import get_name_acronym


class Competitor(
    AbstractAcronym,
    AbstractBaseModel,
    AbstractComment,
    AbstractLocation,
    AbstractName,
    AbstractUniformResourceLocator
):
    """Model to track competitive companies with business intelligence and relationships."""

    # Business Intelligence Fields
    primary_products: str | None = models.CharField(max_length=255, null=True, blank=True)
    market_segment: str | None = models.CharField(max_length=255, null=True, blank=True)
    employee_count_tier: str | None = models.CharField(max_length=255, choices=EMPLOYEE_COUNT_TIER_CHOICES, null=True, blank=True)
    revenue_tier: str | None = models.CharField(max_length=255, choices=REVENUE_TIER_CHOICES, null=True, blank=True)
    year_founded: int | None = models.IntegerField(null=True, blank=True)

    # Relationships
    competing_applications: set[Application] | None = models.ManyToManyField(
        Application,
        blank=True,
        related_name='competitors'
    )
    organizations: set[Organization] | None = models.ManyToManyField(
        Organization,
        blank=True,
        related_name='competitors'
    )

    def __str__(self) -> str:
        return get_name_acronym(acronym=self.acronym, name=self.name)

    @property
    def application_count(self) -> int:
        """Count of related applications."""
        return self.competing_applications.count() if self.competing_applications else 0

    @property
    def organization_count(self) -> int:
        """Count of related organizations."""
        return self.organizations.count() if self.organizations else 0

    class Meta:
        ordering = ['name', '-id']
        verbose_name = "Competitor"
        verbose_name_plural = "Competitors"
