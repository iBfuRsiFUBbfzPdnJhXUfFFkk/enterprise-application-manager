from django_generic_model_fields.create_generic_date import create_generic_date
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_integer import create_generic_integer

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.enums.priority_choices import PRIORITY_CHOICES
from core.models.common.enums.task_status_choices import (
    TASK_STATUS_CHOICES,
    TASK_STATUS_COMPLETED,
    TASK_STATUS_IN_PROGRESS,
    TASK_STATUS_TO_DO,
)


class Task(AbstractBaseModel, AbstractComment, AbstractName):
    priority = create_generic_enum(choices=PRIORITY_CHOICES)
    status = create_generic_enum(choices=TASK_STATUS_CHOICES)
    date_completed = create_generic_date()
    order = create_generic_integer()

    @property
    def is_completed(self) -> bool:
        """Returns True if task is completed"""
        return self.status == TASK_STATUS_COMPLETED

    @property
    def is_in_progress(self) -> bool:
        """Returns True if task is in progress"""
        return self.status == TASK_STATUS_IN_PROGRESS

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['order', 'id']
