from decimal import Decimal

from django.db import models
from django_generic_model_fields.create_generic_decimal import create_generic_decimal
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
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

    # Developer counts for duration estimation
    junior_developer_count = create_generic_integer()
    mid_developer_count = create_generic_integer()
    senior_developer_count = create_generic_integer()
    lead_developer_count = create_generic_integer()
    reviewer_count = create_generic_integer()

    # Base hours (before uncertainty) - includes dev + code review + testing
    def get_base_hours_junior(self):
        """Calculate total base junior developer hours from all items (dev + code review + testing, before uncertainty)."""
        return sum(
            (item.hours_junior or 0) +
            (item.code_review_hours_junior or 0) +
            (item.tests_hours_junior or 0)
            for item in self.items.all()
        )

    def get_base_hours_mid(self):
        """Calculate total base mid-level developer hours from all items (dev + code review + testing, before uncertainty)."""
        return sum(
            (item.hours_mid or 0) +
            (item.code_review_hours_mid or 0) +
            (item.tests_hours_mid or 0)
            for item in self.items.all()
        )

    def get_base_hours_senior(self):
        """Calculate total base senior developer hours from all items (dev + code review + testing, before uncertainty)."""
        return sum(
            (item.hours_senior or 0) +
            (item.code_review_hours_senior or 0) +
            (item.tests_hours_senior or 0)
            for item in self.items.all()
        )

    def get_base_hours_lead(self):
        """Calculate total base lead developer hours from all items (dev + code review + testing, before uncertainty)."""
        return sum(
            (item.hours_lead or 0) +
            (item.code_review_hours_lead or 0) +
            (item.tests_hours_lead or 0)
            for item in self.items.all()
        )

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

    # Duration estimation methods (based on 40-hour work week)
    def get_duration_weeks_junior(self):
        """Calculate duration in weeks for junior developers (grand total / count / 40)."""
        count = self.junior_developer_count or 0
        if count == 0:
            return None
        hours_per_dev = self.get_grand_total_hours_junior() / Decimal(str(count))
        return hours_per_dev / Decimal('40.0')

    def get_duration_months_junior(self):
        """Calculate duration in months for junior developers (weeks / 4.33)."""
        weeks = self.get_duration_weeks_junior()
        if weeks is None:
            return None
        return weeks / Decimal('4.33')  # 52 weeks / 12 months ≈ 4.33

    def get_duration_weeks_mid(self):
        """Calculate duration in weeks for mid-level developers (grand total / count / 40)."""
        count = self.mid_developer_count or 0
        if count == 0:
            return None
        hours_per_dev = self.get_grand_total_hours_mid() / Decimal(str(count))
        return hours_per_dev / Decimal('40.0')

    def get_duration_months_mid(self):
        """Calculate duration in months for mid-level developers (weeks / 4.33)."""
        weeks = self.get_duration_weeks_mid()
        if weeks is None:
            return None
        return weeks / Decimal('4.33')

    def get_duration_weeks_senior(self):
        """Calculate duration in weeks for senior developers (grand total / count / 40)."""
        count = self.senior_developer_count or 0
        if count == 0:
            return None
        hours_per_dev = self.get_grand_total_hours_senior() / Decimal(str(count))
        return hours_per_dev / Decimal('40.0')

    def get_duration_months_senior(self):
        """Calculate duration in months for senior developers (weeks / 4.33)."""
        weeks = self.get_duration_weeks_senior()
        if weeks is None:
            return None
        return weeks / Decimal('4.33')

    def get_duration_weeks_lead(self):
        """Calculate duration in weeks for lead developers (grand total / count / 40)."""
        count = self.lead_developer_count or 0
        if count == 0:
            return None
        hours_per_dev = self.get_grand_total_hours_lead() / Decimal(str(count))
        return hours_per_dev / Decimal('40.0')

    def get_duration_months_lead(self):
        """Calculate duration in months for lead developers (weeks / 4.33)."""
        weeks = self.get_duration_weeks_lead()
        if weeks is None:
            return None
        return weeks / Decimal('4.33')

    def get_duration_weeks_reviewer(self):
        """Calculate duration in weeks for code reviewers (grand total / count / 40)."""
        count = self.reviewer_count or 0
        if count == 0:
            return None
        hours_per_dev = self.get_grand_total_reviewer_hours() / Decimal(str(count))
        return hours_per_dev / Decimal('40.0')

    def get_duration_months_reviewer(self):
        """Calculate duration in months for code reviewers (weeks / 4.33)."""
        weeks = self.get_duration_weeks_reviewer()
        if weeks is None:
            return None
        return weeks / Decimal('4.33')

    # Combined project duration (for mixed teams working in parallel)
    def get_combined_project_duration_weeks(self):
        """
        Calculate overall project duration in weeks for a mixed team.
        Each level works on their portion in parallel; project completes when slowest level finishes.
        Returns None if no developer counts are set.
        """
        durations = []

        if self.junior_developer_count and self.junior_developer_count > 0:
            durations.append(self.get_duration_weeks_junior())

        if self.mid_developer_count and self.mid_developer_count > 0:
            durations.append(self.get_duration_weeks_mid())

        if self.senior_developer_count and self.senior_developer_count > 0:
            durations.append(self.get_duration_weeks_senior())

        if self.lead_developer_count and self.lead_developer_count > 0:
            durations.append(self.get_duration_weeks_lead())

        # Reviewer time runs in parallel with dev work, so we include it
        if self.reviewer_count and self.reviewer_count > 0:
            durations.append(self.get_duration_weeks_reviewer())

        # Filter out None values and return max (bottleneck)
        valid_durations = [d for d in durations if d is not None]
        if not valid_durations:
            return None

        return max(valid_durations)

    def get_combined_project_duration_months(self):
        """Calculate overall project duration in months for a mixed team."""
        weeks = self.get_combined_project_duration_weeks()
        if weeks is None:
            return None
        return weeks / Decimal('4.33')

    def get_bottleneck_level(self):
        """
        Identify which developer level is the bottleneck (takes longest).
        Returns tuple of (level_name, duration_weeks) or None if no counts set.
        """
        durations_by_level = []

        if self.junior_developer_count and self.junior_developer_count > 0:
            durations_by_level.append(('Junior', self.get_duration_weeks_junior()))

        if self.mid_developer_count and self.mid_developer_count > 0:
            durations_by_level.append(('Mid', self.get_duration_weeks_mid()))

        if self.senior_developer_count and self.senior_developer_count > 0:
            durations_by_level.append(('Senior', self.get_duration_weeks_senior()))

        if self.lead_developer_count and self.lead_developer_count > 0:
            durations_by_level.append(('Lead', self.get_duration_weeks_lead()))

        if self.reviewer_count and self.reviewer_count > 0:
            durations_by_level.append(('Reviewer', self.get_duration_weeks_reviewer()))

        # Filter out None values
        valid_durations = [(name, dur) for name, dur in durations_by_level if dur is not None]
        if not valid_durations:
            return None

        # Return the level with maximum duration
        return max(valid_durations, key=lambda x: x[1])

    def get_total_team_size(self):
        """Calculate total number of developers across all levels (excluding reviewers)."""
        return (
            (self.junior_developer_count or 0) +
            (self.mid_developer_count or 0) +
            (self.senior_developer_count or 0) +
            (self.lead_developer_count or 0)
        )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['-id']
        verbose_name = 'Estimation'
        verbose_name_plural = 'Estimations'
