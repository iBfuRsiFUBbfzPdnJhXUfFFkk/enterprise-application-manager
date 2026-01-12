
from django.db import models
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
    priority = models.CharField(max_length=255, choices=PRIORITY_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=255, choices=TASK_STATUS_CHOICES, null=True, blank=True)
    date_completed = models.DateField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)

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
