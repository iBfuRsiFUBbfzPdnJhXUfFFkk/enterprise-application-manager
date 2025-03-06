from typing import cast, Optional

from django.db.models import QuerySet
from math import ceil

from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.field_factories.create_generic_decimal import create_generic_decimal
from core.models.common.field_factories.create_generic_fk import create_generic_fk
from core.models.common.field_factories.create_generic_integer import create_generic_integer
from core.models.person import Person
from core.models.sprint import Sprint
from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.this_server_configuration.get_current_server_configuration import get_current_server_configuration


class KeyPerformanceIndicatorSprint(BaseModel, Comment):
    cached_capacity_adjusted = create_generic_integer()
    cached_capacity_base_velocity = create_generic_decimal()
    cached_capacity_per_day = create_generic_decimal()
    cached_commitment_accuracy = create_generic_decimal()
    capacity_base = create_generic_integer()
    number_of_code_lines_added = create_generic_integer()
    number_of_code_lines_removed = create_generic_integer()
    number_of_comments_made = create_generic_integer()
    number_of_context_switches = create_generic_integer()
    number_of_issues_written = create_generic_integer()
    number_of_merge_requests_approved = create_generic_integer()
    number_of_paid_time_off_days = create_generic_integer()
    number_of_story_points_committed_to = create_generic_integer()
    number_of_story_points_delivered = create_generic_integer()
    number_of_threads_made = create_generic_integer()
    person_developer = create_generic_fk(to=Person)
    sprint = create_generic_fk(to=Sprint)

    @property
    def adjusted_capacity(self) -> int:
        number_of_business_days_in_sprint: int = 0
        number_of_holidays_during_sprint: int = 0
        sprint: Sprint | None = self.sprint
        if sprint is not None:
            number_of_business_days_in_sprint: int = sprint.coerced_number_of_business_days_in_sprint
            number_of_holidays_during_sprint: int = sprint.number_of_holidays_during_sprint or 0
        effective_days: int = (
                number_of_business_days_in_sprint
                - number_of_holidays_during_sprint
                - (self.number_of_paid_time_off_days or 0)
        )
        capacity: int = max(0, ceil(effective_days * self.capacity_per_day))
        value: int = min(self.coerced_base_capacity, capacity)
        self.cached_capacity_adjusted = value
        self.save()
        return value

    @property
    def capacity_based_velocity(self) -> float:
        value: float = 0
        number_of_story_points_delivered: int = self.number_of_story_points_delivered or 0
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
            number=self.coerced_base_capacity / number_of_business_days_in_sprint
        )
        self.cached_capacity_per_day = value
        self.save()
        return value

    @property
    def coerced_base_capacity(self) -> int:
        if self.capacity_base is not None:
            return self.capacity_base
        person: Person | None = self.person_developer
        if person is not None:
            return person.coerced_base_capacity
        current_server_configuration: ThisServerConfiguration | None = get_current_server_configuration()
        return current_server_configuration.coerced_base_capacity

    @property
    def commitment_accuracy(self) -> float:
        value: float = 0
        number_of_story_points_delivered: int = self.number_of_story_points_delivered or 0
        number_of_story_points_committed_to: int = self.number_of_story_points_committed_to or 0
        if number_of_story_points_committed_to > 0:
            value: float = round(
                ndigits=2,
                number=number_of_story_points_delivered / number_of_story_points_committed_to
            )
        self.cached_commitment_accuracy = value
        self.save()
        return value

    @staticmethod
    def for_person(person: Person) -> QuerySet['KeyPerformanceIndicatorSprint']:
        return cast(
            typ=QuerySet[KeyPerformanceIndicatorSprint],
            val=KeyPerformanceIndicatorSprint.objects.filter(
                person_developer=person,
            ).order_by('-sprint__date_end')
        )

    @staticmethod
    def get_by_uuid(uuid: str) -> Optional['KeyPerformanceIndicatorSprint']:
        return KeyPerformanceIndicatorSprint.objects.filter(enumeration_attack_uuid=uuid).first()

    def __str__(self):
        return f"{str(self.id)} | {str(self.person_developer)} | {str(self.sprint)}"

    class Meta:
        ordering = ['-id']
