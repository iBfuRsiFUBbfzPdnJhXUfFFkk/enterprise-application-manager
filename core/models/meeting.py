from datetime import datetime

from django.db import models
from django.utils import timezone

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_location import AbstractLocation
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.enums.meeting_status_choices import MEETING_STATUS_CHOICES
from core.models.common.enums.meeting_type_choices import MEETING_TYPE_CHOICES

class Meeting(AbstractBaseModel, AbstractComment, AbstractName, AbstractLocation):
    datetime_start = models.DateTimeField(null=True, blank=True)
    datetime_end = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    agenda = models.TextField(null=True, blank=True)
    minutes = models.TextField(null=True, blank=True)
    organizer = models.ForeignKey('Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='meetings_organized')
    attendees = models.ManyToManyField('Person', blank=True, related_name='meetings_attended')
    actual_attendees = models.ManyToManyField('Person', blank=True, related_name='meetings_actually_attended')
    application = models.ForeignKey('Application', on_delete=models.SET_NULL, null=True, blank=True, related_name='meetings')
    project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, blank=True, related_name='meetings')
    meeting_type = models.CharField(max_length=255, choices=MEETING_TYPE_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=255, choices=MEETING_STATUS_CHOICES, null=True, blank=True)
    virtual_meeting_url = models.CharField(max_length=255, null=True, blank=True)

    @property
    def duration_hours(self) -> float:
        if self.datetime_start and self.datetime_end:
            delta = self.datetime_end - self.datetime_start
            return round(delta.total_seconds() / 3600, 2)
        return 0.0

    @property
    def is_in_progress(self) -> bool:
        now = timezone.now()
        if self.datetime_start and self.datetime_end:
            return self.datetime_start <= now <= self.datetime_end
        return False

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ['-datetime_start', '-id']
        indexes = [
            models.Index(fields=['datetime_start']),
            models.Index(fields=['datetime_end']),
            models.Index(fields=['status']),
            models.Index(fields=['meeting_type']),
        ]
