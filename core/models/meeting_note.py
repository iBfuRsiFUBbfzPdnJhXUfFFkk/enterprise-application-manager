from django.db import models
from django.db.models import DateTimeField

from core.models.common.abstract.abstract_base_model import AbstractBaseModel

NOTE_TYPE_CHOICES = (
    ('note', 'Note'),
    ('quote', 'Quote'),
)

class MeetingNote(AbstractBaseModel):
    """Notes and quotes captured during a meeting."""

    meeting = models.ForeignKey('core.Meeting', on_delete=models.SET_NULL, null=True, blank=True, related_name='notes')
    note_type: str = models.CharField(max_length=255, choices=NOTE_TYPE_CHOICES, null=True, blank=True)
    content: str = models.TextField()
    person = models.ForeignKey('core.Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='meeting_notes')  # Optional - person who said the quote
    datetime_created = DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """Set default note_type to 'note' if not specified."""
        if not self.note_type:
            self.note_type = 'note'
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['datetime_created', 'id']
        verbose_name = 'Meeting Note'
        verbose_name_plural = 'Meeting Notes'
        indexes = [
            models.Index(fields=['note_type']),
            models.Index(fields=['datetime_created']),
        ]

    def __str__(self) -> str:
        if self.note_type == 'quote' and self.person:
            return f'Quote from {self.person.full_name}: {self.content[:50]}'
        return f'Note: {self.content[:50]}'
