from decimal import Decimal

from django.db import models
from django_generic_model_fields.create_generic_decimal import create_generic_decimal
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_m2m import create_generic_m2m
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

    # Related links
    links = create_generic_m2m(
        to='Link',
        related_name='estimations'
    )

    # Contingency padding as a percentage (e.g., 20 for 20%)
    contingency_padding_percent = create_generic_decimal()

    # Story points modifier for team calibration (multiplier applied to auto-calculated story points)
    # Default 1.0 = standard calculation (1 point ≈ 4 hours)
    # > 1.0 = increases story points, < 1.0 = decreases story points
    story_points_modifier = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.0,
        help_text="Multiplier for auto-calculated story points to calibrate to your team's velocity (default: 1.0)"
    )

    # Sprint duration in weeks (for sprint calculation)
    sprint_duration_weeks = create_generic_integer()

    # Developer counts for duration estimation
    junior_developer_count = create_generic_integer()
    mid_developer_count = create_generic_integer()
    senior_developer_count = create_generic_integer()
    lead_developer_count = create_generic_integer()

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

    # Best case hours (minimum uncertainty - 1.1x multiplier)
    def get_total_hours_junior_best_case(self):
        """Calculate total junior developer hours with best case uncertainty (1.1x)."""
        return sum(item.get_base_hours_junior() * Decimal('1.1') for item in self.items.all())

    def get_total_hours_mid_best_case(self):
        """Calculate total mid-level developer hours with best case uncertainty (1.1x)."""
        return sum(item.get_base_hours_mid() * Decimal('1.1') for item in self.items.all())

    def get_total_hours_senior_best_case(self):
        """Calculate total senior developer hours with best case uncertainty (1.1x)."""
        return sum(item.get_base_hours_senior() * Decimal('1.1') for item in self.items.all())

    def get_total_hours_lead_best_case(self):
        """Calculate total lead developer hours with best case uncertainty (1.1x)."""
        return sum(item.get_base_hours_lead() * Decimal('1.1') for item in self.items.all())

    # Worst case hours (maximum uncertainty - 4.0x multiplier)
    def get_total_hours_junior_worst_case(self):
        """Calculate total junior developer hours with worst case uncertainty (4.0x)."""
        return sum(item.get_base_hours_junior() * Decimal('4.0') for item in self.items.all())

    def get_total_hours_mid_worst_case(self):
        """Calculate total mid-level developer hours with worst case uncertainty (4.0x)."""
        return sum(item.get_base_hours_mid() * Decimal('4.0') for item in self.items.all())

    def get_total_hours_senior_worst_case(self):
        """Calculate total senior developer hours with worst case uncertainty (4.0x)."""
        return sum(item.get_base_hours_senior() * Decimal('4.0') for item in self.items.all())

    def get_total_hours_lead_worst_case(self):
        """Calculate total lead developer hours with worst case uncertainty (4.0x)."""
        return sum(item.get_base_hours_lead() * Decimal('4.0') for item in self.items.all())

    # Contingency padding per level (applied to base hours only)
    def get_contingency_hours_junior(self):
        """Calculate contingency hours for junior level (applied to base hours only)."""
        return self.get_base_hours_junior() * (self.contingency_padding_percent / 100)

    def get_contingency_hours_mid(self):
        """Calculate contingency hours for mid level (applied to base hours only)."""
        return self.get_base_hours_mid() * (self.contingency_padding_percent / 100)

    def get_contingency_hours_senior(self):
        """Calculate contingency hours for senior level (applied to base hours only)."""
        return self.get_base_hours_senior() * (self.contingency_padding_percent / 100)

    def get_contingency_hours_lead(self):
        """Calculate contingency hours for lead level (applied to base hours only)."""
        return self.get_base_hours_lead() * (self.contingency_padding_percent / 100)

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

    # Grand totals for best case (with best case hours + contingency)
    def get_grand_total_hours_junior_best_case(self):
        """Calculate grand total junior hours for best case scenario (1.1x uncertainty + contingency)."""
        return self.get_total_hours_junior_best_case() + self.get_contingency_hours_junior()

    def get_grand_total_hours_mid_best_case(self):
        """Calculate grand total mid-level hours for best case scenario (1.1x uncertainty + contingency)."""
        return self.get_total_hours_mid_best_case() + self.get_contingency_hours_mid()

    def get_grand_total_hours_senior_best_case(self):
        """Calculate grand total senior hours for best case scenario (1.1x uncertainty + contingency)."""
        return self.get_total_hours_senior_best_case() + self.get_contingency_hours_senior()

    def get_grand_total_hours_lead_best_case(self):
        """Calculate grand total lead hours for best case scenario (1.1x uncertainty + contingency)."""
        return self.get_total_hours_lead_best_case() + self.get_contingency_hours_lead()

    # Grand totals for worst case (with worst case hours + contingency)
    def get_grand_total_hours_junior_worst_case(self):
        """Calculate grand total junior hours for worst case scenario (4.0x uncertainty + contingency)."""
        return self.get_total_hours_junior_worst_case() + self.get_contingency_hours_junior()

    def get_grand_total_hours_mid_worst_case(self):
        """Calculate grand total mid-level hours for worst case scenario (4.0x uncertainty + contingency)."""
        return self.get_total_hours_mid_worst_case() + self.get_contingency_hours_mid()

    def get_grand_total_hours_senior_worst_case(self):
        """Calculate grand total senior hours for worst case scenario (4.0x uncertainty + contingency)."""
        return self.get_total_hours_senior_worst_case() + self.get_contingency_hours_senior()

    def get_grand_total_hours_lead_worst_case(self):
        """Calculate grand total lead hours for worst case scenario (4.0x uncertainty + contingency)."""
        return self.get_total_hours_lead_worst_case() + self.get_contingency_hours_lead()

    # Average across levels (optional aggregate view)
    def get_average_hours_with_uncertainty(self):
        """
        Calculate average hours across all developer levels with uncertainty applied.
        This is an optional aggregate view since hours per level are alternatives, not additive.
        """
        return sum(item.get_average_hours_with_uncertainty() for item in self.items.all())

    # Story points total
    def get_total_story_points(self):
        """Calculate total story points across all items."""
        return sum(item.story_points or 0 for item in self.items.all())

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

    # Best case combined project duration
    def get_combined_project_duration_weeks_best_case(self):
        """
        Calculate best case project duration in weeks for a mixed team.
        Uses best case hours (1.1x uncertainty) for all items.
        """
        durations = []

        if self.junior_developer_count and self.junior_developer_count > 0:
            hours_per_dev = self.get_grand_total_hours_junior_best_case() / Decimal(str(self.junior_developer_count))
            durations.append(hours_per_dev / Decimal('40.0'))

        if self.mid_developer_count and self.mid_developer_count > 0:
            hours_per_dev = self.get_grand_total_hours_mid_best_case() / Decimal(str(self.mid_developer_count))
            durations.append(hours_per_dev / Decimal('40.0'))

        if self.senior_developer_count and self.senior_developer_count > 0:
            hours_per_dev = self.get_grand_total_hours_senior_best_case() / Decimal(str(self.senior_developer_count))
            durations.append(hours_per_dev / Decimal('40.0'))

        if self.lead_developer_count and self.lead_developer_count > 0:
            hours_per_dev = self.get_grand_total_hours_lead_best_case() / Decimal(str(self.lead_developer_count))
            durations.append(hours_per_dev / Decimal('40.0'))

        valid_durations = [d for d in durations if d is not None]
        if not valid_durations:
            return None

        return max(valid_durations)

    def get_combined_project_duration_months_best_case(self):
        """Calculate best case project duration in months for a mixed team."""
        weeks = self.get_combined_project_duration_weeks_best_case()
        if weeks is None:
            return None
        return weeks / Decimal('4.33')

    # Worst case combined project duration
    def get_combined_project_duration_weeks_worst_case(self):
        """
        Calculate worst case project duration in weeks for a mixed team.
        Uses worst case hours (4.0x uncertainty) for all items.
        """
        durations = []

        if self.junior_developer_count and self.junior_developer_count > 0:
            hours_per_dev = self.get_grand_total_hours_junior_worst_case() / Decimal(str(self.junior_developer_count))
            durations.append(hours_per_dev / Decimal('40.0'))

        if self.mid_developer_count and self.mid_developer_count > 0:
            hours_per_dev = self.get_grand_total_hours_mid_worst_case() / Decimal(str(self.mid_developer_count))
            durations.append(hours_per_dev / Decimal('40.0'))

        if self.senior_developer_count and self.senior_developer_count > 0:
            hours_per_dev = self.get_grand_total_hours_senior_worst_case() / Decimal(str(self.senior_developer_count))
            durations.append(hours_per_dev / Decimal('40.0'))

        if self.lead_developer_count and self.lead_developer_count > 0:
            hours_per_dev = self.get_grand_total_hours_lead_worst_case() / Decimal(str(self.lead_developer_count))
            durations.append(hours_per_dev / Decimal('40.0'))

        valid_durations = [d for d in durations if d is not None]
        if not valid_durations:
            return None

        return max(valid_durations)

    def get_combined_project_duration_months_worst_case(self):
        """Calculate worst case project duration in months for a mixed team."""
        weeks = self.get_combined_project_duration_weeks_worst_case()
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

    def get_sprint_count(self):
        """
        Calculate the number of sprints needed to complete the project.
        Based on combined project duration divided by sprint duration.
        Returns None if sprint duration or project duration cannot be calculated.
        """
        if not self.sprint_duration_weeks or self.sprint_duration_weeks <= 0:
            return None

        duration_weeks = self.get_combined_project_duration_weeks()
        if duration_weeks is None:
            return None

        # Calculate sprints and round up (can't have partial sprints)
        import math
        return math.ceil(float(duration_weeks) / float(self.sprint_duration_weeks))

    def get_required_team_velocity_per_sprint(self):
        """
        Calculate the required team velocity (story points per sprint) to complete the estimation on time.
        This is the total story points divided by the number of sprints.
        Returns None if sprint count cannot be calculated.
        """
        sprint_count = self.get_sprint_count()
        if sprint_count is None or sprint_count == 0:
            return None

        total_story_points = self.get_total_story_points()
        return Decimal(str(total_story_points)) / Decimal(str(sprint_count))

    def get_required_velocity_per_developer_per_sprint(self):
        """
        Calculate the required velocity per developer per sprint.
        This is the total story points divided by (sprint count * team size).
        Helps assess if the individual workload is reasonable.
        Returns None if team size is 0 or sprint count cannot be calculated.
        """
        sprint_count = self.get_sprint_count()
        team_size = self.get_total_team_size()

        if sprint_count is None or sprint_count == 0 or team_size == 0:
            return None

        total_story_points = self.get_total_story_points()
        return Decimal(str(total_story_points)) / (Decimal(str(sprint_count)) * Decimal(str(team_size)))

    def get_required_velocity_per_week(self):
        """
        Calculate the required velocity per week (story points per week).
        Alternative view for teams that think in weekly rather than sprint cadences.
        Returns None if project duration cannot be calculated.
        """
        duration_weeks = self.get_combined_project_duration_weeks()
        if duration_weeks is None or duration_weeks == 0:
            return None

        total_story_points = self.get_total_story_points()
        return Decimal(str(total_story_points)) / duration_weeks

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['-id']
        verbose_name = 'Estimation'
        verbose_name_plural = 'Estimations'
