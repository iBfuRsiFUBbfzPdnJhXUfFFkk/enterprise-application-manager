from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_m2m import create_generic_m2m
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

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
    primary_products: str | None = create_generic_varchar()
    market_segment: str | None = create_generic_varchar()
    employee_count_tier: str | None = create_generic_enum(choices=EMPLOYEE_COUNT_TIER_CHOICES)
    revenue_tier: str | None = create_generic_enum(choices=REVENUE_TIER_CHOICES)
    year_founded: int | None = create_generic_integer()

    # Relationships
    competing_applications: set[Application] | None = create_generic_m2m(
        related_name='competitors',
        to=Application
    )
    organizations: set[Organization] | None = create_generic_m2m(
        related_name='competitors',
        to=Organization
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
