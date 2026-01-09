from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.enums.action_item_status_choices import ACTION_ITEM_STATUS_CHOICES
from core.models.common.enums.priority_choices import PRIORITY_CHOICES
from django_generic_model_fields.create_generic_date import create_generic_date
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_text import create_generic_text


class MeetingActionItem(AbstractBaseModel, AbstractComment, AbstractName):
    description = create_generic_text()
    due_date = create_generic_date()
    meeting = create_generic_fk(to='Meeting', related_name='action_items')
    assignee = create_generic_fk(to='Person', related_name='action_items_assigned')
    priority = create_generic_enum(choices=PRIORITY_CHOICES)
    status = create_generic_enum(choices=ACTION_ITEM_STATUS_CHOICES)
    date_completed = create_generic_date()

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ['status', '-priority', 'due_date', '-id']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['due_date']),
        ]
