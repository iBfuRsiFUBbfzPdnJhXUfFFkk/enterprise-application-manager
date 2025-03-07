from django.db.models import QuerySet
from math import ceil

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_scrum_capacity_base import AbstractScrumCapacityBase
from core.models.common.field_factories.create_generic_decimal import create_generic_decimal
from core.models.common.field_factories.create_generic_fk import create_generic_fk
from core.models.common.field_factories.create_generic_integer import create_generic_integer
from core.models.person import Person
from core.models.sprint import Sprint
from core.models.this_server_configuration import ThisServerConfiguration
from kpi.utilities.cast_query_set import cast_query_set
from kpi.utilities.coerce_float import coerce_float
from kpi.utilities.coerce_integer import coerce_integer
from kpi.utilities.save_divide import save_divide


class KeyPerformanceIndicatorSprint(
    AbstractBaseModel,
    AbstractComment,
    AbstractScrumCapacityBase,
):
    cached_capacity_adjusted: int | None = create_generic_integer()
    cached_capacity_base_velocity: float | None = create_generic_decimal()
    cached_capacity_per_day: float | None = create_generic_decimal()
    cached_commitment_accuracy: float | None = create_generic_decimal()
    number_of_code_lines_added: int | None = create_generic_integer()
    number_of_code_lines_removed: int | None = create_generic_integer()
    number_of_comments_made: int | None = create_generic_integer()
    number_of_context_switches: int | None = create_generic_integer()
    number_of_issues_written: int | None = create_generic_integer()
    number_of_merge_requests_approved: int | None = create_generic_integer()
    number_of_paid_time_off_days: int | None = create_generic_integer()
    number_of_story_points_committed_to: int | None = create_generic_integer()
    number_of_story_points_delivered: int | None = create_generic_integer()
    number_of_threads_made: int | None = create_generic_integer()
    person_developer: Person | None = create_generic_fk(to=Person)
    sprint: Sprint | None = create_generic_fk(to=Sprint)

    @property
    def adjusted_capacity(self) -> int:
        number_of_holidays_during_sprint: int = 0
        sprint: Sprint | None = self.sprint
        if sprint is not None:
            number_of_holidays_during_sprint: int = sprint.number_of_holidays_during_sprint or 0
        effective_days: int = (
                sprint.coerced_number_of_business_days_in_sprint
                - number_of_holidays_during_sprint
                - self.coerced_number_of_paid_time_off_days
        )
        capacity: int = max(0, ceil(effective_days * self.capacity_per_day))
        value: int = min(self.coerced_scrum_capacity_base, capacity)
        self.cached_capacity_adjusted = value
        self.save()
        return value

    @property
    def capacity_based_velocity(self) -> float:
        value: float = 0
        number_of_story_points_delivered: int = self.coerced_number_of_story_points_delivered
        adjusted_capacity: int = self.adjusted_capacity
        if adjusted_capacity > 0:
            value: float = round(
                ndigits=2,
                number=number_of_story_points_delivered / adjusted_capacity
            )
        self.cached_capacity_based_velocity = value
        self.save()
        return value

    @property
    def capacity_per_day(self) -> float:
        number_of_business_days_in_sprint: int = 0
        sprint: Sprint | None = self.sprint
        if sprint is not None:
            number_of_business_days_in_sprint: int = sprint.coerced_number_of_business_days_in_sprint
        if number_of_business_days_in_sprint == 0:
            self.cached_capacity_per_day = 0
            self.save()
            return 0
        value: float = round(
            ndigits=2,
            number=self.coerced_scrum_capacity_base / number_of_business_days_in_sprint
        )
        self.cached_capacity_per_day = value
        self.save()
        return value

    @property
    def coerced_cached_capacity_adjusted(self) -> int:
        return coerce_integer(value=self.cached_capacity_adjusted)

    @property
    def coerced_cached_capacity_base_velocity(self) -> float:
        return coerce_float(value=self.cached_capacity_base_velocity)

    @property
    def coerced_cached_capacity_per_day(self) -> float:
        return coerce_float(value=self.cached_capacity_per_day)

    @property
    def coerced_cached_commitment_accuracy(self) -> float:
        return coerce_float(value=self.cached_commitment_accuracy)

    @property
    def coerced_scrum_capacity_base(self) -> int:
        if self.scrum_capacity_base is not None:
            return self.scrum_capacity_base
        person: Person | None = self.person_developer
        if person is not None:
            return person.coerced_scrum_capacity_base
        return ThisServerConfiguration.current().coerced_scrum_capacity_base

    @property
    def coerced_number_of_code_lines_added(self) -> int:
        return coerce_integer(value=self.number_of_code_lines_added)

    @property
    def coerced_number_of_code_lines_removed(self) -> int:
        return coerce_integer(value=self.number_of_code_lines_removed)

    @property
    def coerced_number_of_comments_made(self) -> int:
        return coerce_integer(value=self.number_of_comments_made)

    @property
    def coerced_number_of_context_switches(self) -> int:
        return coerce_integer(value=self.number_of_context_switches)

    @property
    def coerced_number_of_issues_written(self) -> int:
        return coerce_integer(value=self.number_of_issues_written)

    @property
    def coerced_number_of_merge_requests_approved(self) -> int:
        return coerce_integer(value=self.number_of_merge_requests_approved)

    @property
    def coerced_number_of_paid_time_off_days(self) -> int:
        return coerce_integer(value=self.number_of_paid_time_off_days)

    @property
    def coerced_number_of_story_points_committed_to(self) -> int:
        return coerce_integer(value=self.number_of_story_points_committed_to)

    @property
    def coerced_number_of_story_points_delivered(self) -> int:
        return coerce_integer(value=self.number_of_story_points_delivered)

    @property
    def coerced_number_of_threads_made(self) -> int:
        return coerce_integer(value=self.number_of_threads_made)

    @property
    def commitment_accuracy(self) -> float:
        value: float = round(
            ndigits=2,
            number=save_divide(
                dividend=self.coerced_number_of_story_points_delivered,
                divisor=self.coerced_number_of_story_points_committed_to,
            )
        )
        self.cached_commitment_accuracy = value
        self.save()
        return value

    @staticmethod
    def from_person(person: Person) -> QuerySet['KeyPerformanceIndicatorSprint']:
        return cast_query_set(
            typ=KeyPerformanceIndicatorSprint,
            val=KeyPerformanceIndicatorSprint.objects.filter(person_developer=person)
        )

    def __str__(self) -> str:
        return f"{str(self.sprint)} - {str(self.person_developer)}"

    class Meta:
        ordering = ['-sprint__date_end', '-id']
