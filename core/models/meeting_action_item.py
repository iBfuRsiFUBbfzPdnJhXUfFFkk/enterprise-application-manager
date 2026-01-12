from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.enums.action_item_status_choices import ACTION_ITEM_STATUS_CHOICES
from core.models.common.enums.priority_choices import PRIORITY_CHOICES

class MeetingActionItem(AbstractBaseModel, AbstractComment, AbstractName):
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    meeting = models.ForeignKey('Meeting', on_delete=models.SET_NULL, null=True, blank=True, related_name='action_items')
    assignee = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='action_items_assigned')
    priority = models.CharField(max_length=255, choices=PRIORITY_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=255, choices=ACTION_ITEM_STATUS_CHOICES, null=True, blank=True)
    date_completed = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ['status', '-priority', 'due_date', '-id']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['due_date']),
        ]
