from django.db.models import QuerySet, Q
from math import ceil

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_scrum_capacity_base import AbstractScrumCapacityBase
from django_generic_model_fields.create_generic_decimal import create_generic_decimal
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from core.models.person import Person
from core.models.sprint import Sprint
from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.cast_query_set import cast_query_set
from core.utilities.coerce_float import coerce_float
from core.utilities.coerce_integer import coerce_integer
from core.utilities.safe_divide import safe_divide
from git_lab.models.git_lab_user import GitLabUser
from scrum.models.scrum_sprint import ScrumSprint


class KeyPerformanceIndicatorSprint(
    AbstractBaseModel,
    AbstractComment,
    AbstractScrumCapacityBase,
):
    cached_capacity_adjusted: int | None = create_generic_integer()
    cached_capacity_base_velocity: float | None = create_generic_decimal()
    cached_capacity_per_day: float | None = create_generic_decimal()
    cached_commitment_accuracy: float | None = create_generic_decimal()
    git_lab_user: GitLabUser | None = create_generic_fk(related_name="kpi_sprints", to=GitLabUser)
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
    scrum_sprint: ScrumSprint | None = create_generic_fk(related_name="kpi_sprints", to=ScrumSprint)
    sprint: Sprint | None = create_generic_fk(to=Sprint)

    @property
    def adjusted_capacity(self) -> int:
        value: int = min(self.coerced_scrum_capacity_base, self.calculated_capacity)
        self.cached_capacity_adjusted = value
        self.save()
        return value

    @property
    def calculated_capacity(self) -> int:
        return max(0, ceil(self.effective_days * self.capacity_per_day))

    @property
    def capacity_based_velocity(self) -> float:
        value: float = round(
            ndigits=2,
            number=safe_divide(
                dividend=self.coerced_number_of_story_points_delivered,
                divisor=self.adjusted_capacity,
            )
        )
        self.cached_capacity_based_velocity = value
        self.save()
        return value

    @property
    def capacity_per_day(self) -> float:
        value: float = round(
            ndigits=2,
            number=safe_divide(
                dividend=self.coerced_scrum_capacity_base,
                divisor=self.coerced_number_of_business_days_in_sprint
            )
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
    def coerced_number_of_business_days_in_sprint(self) -> int:
        if self.sprint is None:
            return ThisServerConfiguration.current().coerced_scrum_number_of_business_days_in_sprint
        return coerce_integer(self.sprint.coerced_number_of_business_days_in_sprint)

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
    def coerced_number_of_holidays_during_sprint(self) -> int:
        if self.sprint is None:
            return 0
        return coerce_integer(self.sprint.number_of_holidays_during_sprint)

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
            number=safe_divide(
                dividend=self.coerced_number_of_story_points_delivered,
                divisor=self.coerced_number_of_story_points_committed_to,
            )
        )
        self.cached_commitment_accuracy = value
        self.save()
        return value

    @property
    def effective_days(self) -> int:
        return (
                self.coerced_number_of_business_days_in_sprint
                - self.coerced_number_of_holidays_during_sprint
                - self.coerced_number_of_paid_time_off_days
        )

    @staticmethod
    def developers_actively_employed() -> QuerySet['KeyPerformanceIndicatorSprint']:
        developers_actively_employed: QuerySet[Person] = Person.developers_actively_employed()
        return cast_query_set(
            typ=KeyPerformanceIndicatorSprint,
            val=KeyPerformanceIndicatorSprint.objects.filter(
                Q(person_developer__in=developers_actively_employed),
                ~Q(person_developer__in=ThisServerConfiguration.current().kpi_developers_to_exclude.all())
            )
        )

    @staticmethod
    def from_person(person: Person) -> QuerySet['KeyPerformanceIndicatorSprint']:
        return cast_query_set(
            typ=KeyPerformanceIndicatorSprint,
            val=KeyPerformanceIndicatorSprint.objects.filter(person_developer=person)
        )

    @staticmethod
    def from_person_current_sprint(person: Person) -> QuerySet['KeyPerformanceIndicatorSprint']:
        return cast_query_set(
            typ=KeyPerformanceIndicatorSprint,
            val=KeyPerformanceIndicatorSprint.objects.filter(
                person_developer=person,
                sprint=Sprint.current_sprint(),
            )
        )

    @staticmethod
    def from_person_last_five_sprints(person: Person) -> QuerySet['KeyPerformanceIndicatorSprint']:
        return cast_query_set(
            typ=KeyPerformanceIndicatorSprint,
            val=KeyPerformanceIndicatorSprint.objects.filter(
                person_developer=person,
                sprint__in=Sprint.last_five_sprints(),
            )
        )

    @staticmethod
    def from_sprint(sprint: Sprint) -> QuerySet['KeyPerformanceIndicatorSprint']:
        return cast_query_set(
            typ=KeyPerformanceIndicatorSprint,
            val=KeyPerformanceIndicatorSprint.developers_actively_employed().filter(sprint=sprint)
        )

    def __str__(self) -> str:
        return f"{str(self.sprint)} - {str(self.person_developer)}"

    class Meta:
        ordering = ['-sprint__date_end', '-id']
        verbose_name = 'Key Performance Indicator (KPI) Sprint'
        verbose_name_plural = 'Key Performance Indicator (KPI) Sprints'
