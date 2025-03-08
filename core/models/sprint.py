from datetime import date
from typing import Optional

from django.db.models import QuerySet

from core.models.common.abstract.abstract_alias import AbstractAlias
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.abstract.abstract_start_end_dates import AbstractStartEndDates
from core.models.common.field_factories.create_generic_decimal import create_generic_decimal
from core.models.common.field_factories.create_generic_integer import create_generic_integer
from core.models.git_lab_iteration import GitLabIteration
from core.models.this_server_configuration import ThisServerConfiguration
from kpi.utilities.cast_query_set import cast_query_set
from kpi.utilities.coerce_integer import coerce_integer
from kpi.utilities.safe_divide import safe_divide
from kpi.utilities.string_or_na import string_or_na


class Sprint(
    AbstractAlias,
    AbstractBaseModel,
    AbstractComment,
    AbstractName,
    AbstractStartEndDates,
):
    cached_accuracy: float | None = create_generic_decimal()
    cached_total_adjusted_capacity: int | None = create_generic_integer()
    cached_total_number_of_merge_requests_approved: int | None = create_generic_integer()
    cached_total_number_of_story_points_delivered: int | None = create_generic_integer()
    cached_total_number_of_story_points_committed_to: int | None = create_generic_integer()
    cached_velocity: float | None = create_generic_decimal()
    number_of_business_days_in_sprint: int | None = create_generic_integer()
    number_of_holidays_during_sprint: int | None = create_generic_integer()

    @property
    def accuracy(self) -> float:
        value: float = round(
            ndigits=2,
            number=safe_divide(
                dividend=self.total_number_of_story_points_delivered,
                divisor=self.total_number_of_story_points_committed_to,
            )
        )
        self.cached_accuracy = value
        self.save()
        return value

    @property
    def coerced_number_of_holidays_during_sprint(self) -> int:
        return coerce_integer(value=self.number_of_holidays_during_sprint)

    @property
    def coerced_number_of_business_days_in_sprint(self) -> int:
        if self.number_of_business_days_in_sprint is not None:
            return self.number_of_business_days_in_sprint
        return ThisServerConfiguration.current().coerced_scrum_number_of_business_days_in_sprint

    @property
    def git_lab_iterations(self) -> QuerySet[GitLabIteration]:
        return cast_query_set(
            typ=GitLabIteration,
            val=GitLabIteration.objects.filter(sprint=self)
        )

    @property
    def git_lab_iteration_ids(self) -> list[int]:
        return [git_lab_iteration.git_lab_id for git_lab_iteration in self.git_lab_iterations]

    @property
    def kpi_sprints(self) -> QuerySet:
        from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint
        return cast_query_set(
            typ=KeyPerformanceIndicatorSprint,
            val=KeyPerformanceIndicatorSprint.objects.filter(sprint=self)
        )

    @property
    def total_adjusted_capacity(self) -> int:
        value: int = sum(kpi_sprint.adjusted_capacity for kpi_sprint in self.kpi_sprints)
        self.cached_total_adjusted_capacity = value
        self.save()
        return value

    @property
    def total_number_of_merge_requests_approved(self) -> int:
        value: int = sum(kpi_sprint.coerced_number_of_merge_requests_approved for kpi_sprint in self.kpi_sprints)
        self.cached_total_number_of_merge_requests_approved = value
        self.save()
        return value

    @property
    def total_number_of_story_points_committed_to(self) -> int:
        value: int = sum(kpi_sprint.coerced_number_of_story_points_committed_to for kpi_sprint in self.kpi_sprints)
        self.cached_total_number_of_story_points_committed_to = value
        self.save()
        return value

    @property
    def total_number_of_story_points_delivered(self) -> int:
        value: int = sum(kpi_sprint.coerced_number_of_story_points_delivered for kpi_sprint in self.kpi_sprints)
        self.cached_total_number_of_story_points_delivered = value
        self.save()
        return value

    @property
    def velocity(self) -> float:
        value: float = round(
            ndigits=2,
            number=safe_divide(
                dividend=self.total_number_of_story_points_delivered,
                divisor=self.total_adjusted_capacity,
            )
        )
        self.cached_velocity = value
        self.save()
        return value

    @staticmethod
    def current_sprint() -> Optional['Sprint']:
        current_date: date = date.today()
        return Sprint.objects.filter(
            date_end__gte=current_date,
            date_start__lte=current_date,
        ).first()

    @staticmethod
    def last_five_sprints() -> QuerySet['Sprint']:
        return cast_query_set(
            typ=Sprint,
            val=Sprint.objects.all().order_by('-date_end')[:5]
        )

    def __str__(self) -> str:
        return f"{string_or_na(self.name)} {self.date_range_string}"

    class Meta:
        ordering = ['-date_end', '-id']
        verbose_name = 'Sprint'
        verbose_name_plural = 'Sprints'
