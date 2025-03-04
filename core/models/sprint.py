from typing import Any

from core.models.common.abstract.abstract_start_end_dates import AbstractStartEndDates
from core.models.common.abstract.alias import Alias
from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.field_factories.create_generic_decimal import create_generic_decimal
from core.models.common.field_factories.create_generic_integer import create_generic_integer


class Sprint(AbstractStartEndDates, Alias, BaseModel, Comment, Name):
    cached_accuracy = create_generic_decimal()
    cached_number_of_code_reviews = create_generic_integer()
    cached_number_of_story_points_delivered = create_generic_integer()
    cached_velocity = create_generic_decimal()
    number_of_business_days_in_sprint = create_generic_integer()
    number_of_holidays_during_sprint = create_generic_integer()

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(args, kwargs)
        self.git_lab_iteration_set = None

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name', '-id']
