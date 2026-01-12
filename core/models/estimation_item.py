from decimal import Decimal

from django.db import models

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
    estimation = models.ForeignKey(
        'Estimation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='items'
    )

    # Order within the estimation
    order = models.IntegerField(null=True, blank=True)

    # Optional group/category for logical organization
    group = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Optional category/group name for organizing related items (e.g., 'Frontend', 'Backend', 'Database')"
    )

    # Item details
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    story_points = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Development hours by developer level
    hours_junior = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hours_mid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hours_senior = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hours_lead = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Code review hours by developer level
    code_review_hours_junior = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    code_review_hours_mid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    code_review_hours_senior = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    code_review_hours_lead = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Code reviewer time (lead dev reviewing others' code - added to lead total only)
    code_reviewer_hours = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Testing hours by developer level
    tests_hours_junior = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tests_hours_mid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tests_hours_senior = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tests_hours_lead = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Cone of Uncertainty - project phase indicator
    cone_of_uncertainty = models.CharField(
        max_length=255,
        choices=CONE_OF_UNCERTAINTY_CHOICES,
        null=True,
        blank=True
    )

    # Complexity level
    complexity_level = models.CharField(
        max_length=255,
        choices=COMPLEXITY_CHOICES,
        null=True,
        blank=True
    )

    # Priority
    priority = models.CharField(
        max_length=255,
        choices=PRIORITY_CHOICES,
        null=True,
        blank=True
    )

    # Related links (many-to-many)
    links = models.ManyToManyField(
        'Link',
        blank=True,
        related_name='estimation_items'
    )

    def get_uncertainty_multiplier(self):
        """
        Get the cone of uncertainty multiplier for this item.
        Returns the multiplier based on project phase, defaults to 1.0 if not set.
        """
        if self.cone_of_uncertainty:
            return self.CONE_OF_UNCERTAINTY_MULTIPLIERS.get(self.cone_of_uncertainty, Decimal('1.0'))
        return Decimal('1.0')

    def get_group_display(self):
        """
        Get the display name for the group.
        Returns the group name if set, otherwise returns 'Ungrouped'.
        """
        return self.group if self.group else 'Ungrouped'

    # Base hours (without uncertainty) for each developer level
    def get_base_hours_junior(self):
        """Calculate base junior hours (dev + code review + tests) without uncertainty."""
        return (self.hours_junior or 0) + (self.code_review_hours_junior or 0) + (self.tests_hours_junior or 0)

    def get_base_hours_mid(self):
        """Calculate base mid-level hours (dev + code review + tests) without uncertainty."""
        return (self.hours_mid or 0) + (self.code_review_hours_mid or 0) + (self.tests_hours_mid or 0)

    def get_base_hours_senior(self):
        """Calculate base senior hours (dev + code review + tests) without uncertainty."""
        return (self.hours_senior or 0) + (self.code_review_hours_senior or 0) + (self.tests_hours_senior or 0)

    def get_base_hours_lead(self):
        """Calculate base lead hours (dev + code review + tests) without uncertainty."""
        return (self.hours_lead or 0) + (self.code_review_hours_lead or 0) + (self.tests_hours_lead or 0)

    # Individual level total hours with cone of uncertainty applied
    def get_junior_hours_with_uncertainty(self):
        """Calculate total junior hours with cone of uncertainty multiplier applied."""
        return self.get_base_hours_junior() * self.get_uncertainty_multiplier()

    def get_mid_hours_with_uncertainty(self):
        """Calculate total mid-level hours with cone of uncertainty multiplier applied."""
        return self.get_base_hours_mid() * self.get_uncertainty_multiplier()

    def get_senior_hours_with_uncertainty(self):
        """Calculate total senior hours with cone of uncertainty multiplier applied."""
        return self.get_base_hours_senior() * self.get_uncertainty_multiplier()

    def get_lead_hours_with_uncertainty(self):
        """Calculate total lead hours with cone of uncertainty multiplier applied."""
        return self.get_base_hours_lead() * self.get_uncertainty_multiplier()

    def get_reviewer_hours(self):
        """Get code reviewer hours without uncertainty padding (assumes lead dev)."""
        return self.code_reviewer_hours or Decimal('0')

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

    def calculate_story_points(self):
        """
        Calculate suggested story points based on lead developer base hours.
        Uses conventional agile wisdom: 1 story point ≈ 4 hours of ideal work time.
        Applies the estimation's story_points_modifier to calibrate for team velocity.
        Rounds to nearest Fibonacci number for practical agile use.
        """
        base_hours = self.get_base_hours_lead()
        if base_hours == 0:
            return Decimal('0')

        # 1 story point = 4 hours of ideal work time (conventional agile wisdom)
        raw_points = base_hours / Decimal('4.0')

        # Apply the estimation's story points modifier if available
        if self.estimation and self.estimation.story_points_modifier:
            raw_points = raw_points * self.estimation.story_points_modifier

        # Round to nearest Fibonacci number
        fibonacci_points = self._round_to_nearest_fibonacci(float(raw_points))

        return Decimal(str(fibonacci_points))

    @staticmethod
    def _round_to_nearest_fibonacci(value):
        """
        Round a value to the nearest Fibonacci number.
        Uses common Fibonacci sequence for story points: 0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, etc.
        """
        # Common Fibonacci sequence used in agile story points
        fib_sequence = [0, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]

        if value <= 0:
            return 0

        # Find the closest Fibonacci number
        closest = min(fib_sequence, key=lambda x: abs(x - value))
        return closest

    def has_overridden_values(self):
        """
        Check if any hour values have been manually overridden from their calculated defaults.
        Returns True if values don't match what would be auto-calculated from lead dev hours.
        This is used to determine whether to show simplified or detailed view on page load.
        """
        # Get lead dev hours as base
        lead_dev_hours = self.hours_lead or Decimal('0')

        # If lead hours is zero, consider it not overridden (new form)
        if lead_dev_hours == 0:
            return False

        # Calculate expected values based on lead dev hours
        # Development hours multipliers: Senior=1.25x, Mid=2x, Junior=3x
        expected_senior = lead_dev_hours * Decimal('1.25')
        expected_mid = lead_dev_hours * Decimal('2.0')
        expected_junior = lead_dev_hours * Decimal('3.0')

        # Code review multiplier: 0.5x of dev hours
        expected_code_review_lead = lead_dev_hours * Decimal('0.5')
        expected_code_review_senior = expected_senior * Decimal('0.5')
        expected_code_review_mid = expected_mid * Decimal('0.5')
        expected_code_review_junior = expected_junior * Decimal('0.5')

        # Testing multiplier: 1x of dev hours
        expected_tests_lead = lead_dev_hours * Decimal('1.0')
        expected_tests_senior = expected_senior * Decimal('1.0')
        expected_tests_mid = expected_mid * Decimal('1.0')
        expected_tests_junior = expected_junior * Decimal('1.0')

        # Code reviewer hours: 1x of lead code review
        expected_code_reviewer = expected_code_review_lead * Decimal('1.0')

        # Helper function to compare with tolerance for floating point rounding
        def is_close(actual, expected, tolerance=Decimal('0.01')):
            """Check if actual value is within tolerance of expected value."""
            actual = actual or Decimal('0')
            diff = abs(actual - expected)
            return diff <= tolerance

        # Check if any value has been overridden (doesn't match calculated value)
        # Only check non-lead fields since lead is the input
        checks = [
            is_close(self.hours_senior, expected_senior),
            is_close(self.hours_mid, expected_mid),
            is_close(self.hours_junior, expected_junior),
            is_close(self.code_review_hours_lead, expected_code_review_lead),
            is_close(self.code_review_hours_senior, expected_code_review_senior),
            is_close(self.code_review_hours_mid, expected_code_review_mid),
            is_close(self.code_review_hours_junior, expected_code_review_junior),
            is_close(self.tests_hours_lead, expected_tests_lead),
            is_close(self.tests_hours_senior, expected_tests_senior),
            is_close(self.tests_hours_mid, expected_tests_mid),
            is_close(self.tests_hours_junior, expected_tests_junior),
            is_close(self.code_reviewer_hours, expected_code_reviewer),
        ]

        # If any value doesn't match, it's been overridden
        return not all(checks)

    def save(self, *args, **kwargs):
        """Auto-assign order for new items."""
        if not self.pk and self.estimation_id and (self.order is None or self.order == 0):
            # Get the max order for this estimation
            max_order = EstimationItem.objects.filter(estimation=self.estimation).aggregate(
                max_order=models.Max('order')
            )['max_order']
            self.order = (max_order or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        if self.title:
            return self.title
        elif self.description:
            return f"{self.description[:50]}..." if len(self.description) > 50 else self.description
        else:
            return f"Item {self.id}"

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Estimation Item'
        verbose_name_plural = 'Estimation Items'
