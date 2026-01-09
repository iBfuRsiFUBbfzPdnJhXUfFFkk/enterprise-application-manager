from django.db import models
from django.db.models import DateTimeField
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_fk import create_generic_fk

from core.models.common.abstract.abstract_base_model import AbstractBaseModel

NOTE_TYPE_CHOICES = (
    ('note', 'Note'),
    ('quote', 'Quote'),
)


class MeetingNote(AbstractBaseModel):
    """Notes and quotes captured during a meeting."""

    meeting = create_generic_fk(to='core.Meeting', related_name='notes')
    note_type: str = create_generic_enum(choices=NOTE_TYPE_CHOICES)
    content: str = models.TextField()
    person = create_generic_fk(to='core.Person', related_name='meeting_notes')  # Optional - person who said the quote
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
