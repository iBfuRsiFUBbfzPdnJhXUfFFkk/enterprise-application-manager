from typing import cast

from django.db.models import QuerySet

from core.models.common.abstract.abstract_start_end_dates import AbstractStartEndDates
from core.models.common.abstract.alias import Alias
from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.field_factories.create_generic_decimal import create_generic_decimal
from core.models.common.field_factories.create_generic_integer import create_generic_integer
from core.models.git_lab_iteration import GitLabIteration


class Sprint(AbstractStartEndDates, Alias, BaseModel, Comment, Name):
    cached_accuracy = create_generic_decimal()
    cached_number_of_code_reviews = create_generic_integer()
    cached_number_of_story_points_delivered = create_generic_integer()
    cached_velocity = create_generic_decimal()
    number_of_business_days_in_sprint = create_generic_integer()
    number_of_holidays_during_sprint = create_generic_integer()

    @property
    def iterations(self) -> QuerySet[GitLabIteration]:
        return cast(typ=QuerySet[GitLabIteration], val=GitLabIteration.objects.filter(sprint=self).all())

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', '-id']
