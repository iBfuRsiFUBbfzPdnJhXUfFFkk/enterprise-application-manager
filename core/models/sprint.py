from datetime import date
from typing import cast, Optional

from django.db.models import QuerySet, Sum

from core.models.common.abstract.abstract_start_end_dates import AbstractStartEndDates
from core.models.common.abstract.alias import Alias
from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.field_factories.create_generic_decimal import create_generic_decimal
from core.models.common.field_factories.create_generic_integer import create_generic_integer
from core.models.git_lab_iteration import GitLabIteration
from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.this_server_configuration.get_current_server_configuration import get_current_server_configuration


class Sprint(AbstractStartEndDates, Alias, BaseModel, Comment, Name):
    cached_accuracy: float | None  = create_generic_decimal()
    cached_number_of_code_reviews: int | None = create_generic_integer()
    cached_number_of_story_points_delivered: int | None = create_generic_integer()
    cached_velocity: float | None  = create_generic_decimal()
    number_of_business_days_in_sprint: int | None = create_generic_integer()
    number_of_holidays_during_sprint: int | None = create_generic_integer()

    @property
    def coerced_number_of_business_days_in_sprint(self) -> int:
        if self.number_of_business_days_in_sprint is not None:
            return self.number_of_business_days_in_sprint
        current_server_configuration: ThisServerConfiguration | None = get_current_server_configuration()
        return current_server_configuration.coerced_scrum_number_of_business_days_in_sprint

    @staticmethod
    def current_sprint() -> Optional['Sprint']:
        current_date: date = date.today()
        return Sprint.objects.filter(
            date_end__gte=current_date,
            date_start__lte=current_date,
        ).first()

    @staticmethod
    def get_by_uuid(uuid: str) -> Optional['Sprint']:
        return Sprint.objects.filter(enumeration_attack_uuid=uuid).first()

    @staticmethod
    def last_five() -> QuerySet['Sprint']:
        current_date: date = date.today()
        return cast(
            typ=QuerySet[Sprint],
            val=Sprint.objects.filter(
                date_end__gte=current_date,
                date_start__lt=current_date,
            ).order_by('-date_end')[:5]
        )

    @property
    def iterations(self) -> QuerySet[GitLabIteration]:
        return cast(typ=QuerySet[GitLabIteration], val=GitLabIteration.objects.filter(sprint=self).all())

    @property
    def iteration_ids(self) -> list[int]:
        return [iteration.git_lab_id for iteration in self.iterations]

    @property
    def kpi_sprints(self) -> QuerySet:
        from kpi.models.key_performance_indicator_sprint import KeyPerformanceIndicatorSprint
        return cast(
            typ=QuerySet[KeyPerformanceIndicatorSprint],
            val=KeyPerformanceIndicatorSprint.objects.filter(sprint=self)
        )

    @property
    def velocity(self):
        kpis = self.kpi_sprints.all()
        total_capacity = sum(kpi.adjusted_capacity for kpi in kpis)
        total_delivered = kpis.aggregate(Sum("number_of_story_points_delivered"))["number_of_story_points_delivered__sum"] or 0
        return round(total_delivered / total_capacity, 2) if total_capacity else 0

    @property
    def accuracy(self):
        kpis = self.kpi_sprints.all()
        total_delivered = kpis.aggregate(Sum("number_of_story_points_delivered"))["number_of_story_points_delivered__sum"] or 0
        total_committed = kpis.aggregate(Sum("number_of_story_points_committed_to"))["number_of_story_points_committed_to__sum"] or 0
        return round(total_delivered / total_committed, 2) if total_committed else 0

    @property
    def delivered(self):
        return self.kpi_sprints.aggregate(Sum("number_of_story_points_delivered"))[
            "number_of_story_points_delivered__sum"] or 0

    @property
    def reviews(self):
        return self.kpi_sprints.aggregate(Sum("number_of_merge_requests_approved"))[
            "number_of_merge_requests_approved__sum"] or 0

    def __str__(self):
        return f"{self.name or 'PLEASE ADD NAME'} ::: {self.date_start} - {self.date_end}"

    class Meta:
        ordering = ['-date_end', '-id']
        verbose_name = 'Sprint'
        verbose_name_plural = 'Sprints'
