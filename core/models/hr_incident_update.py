from django.conf import settings
from django.db import models
from django.db.models import DateTimeField

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment


class HRIncidentUpdate(AbstractBaseModel, AbstractComment):
    hr_incident = models.ForeignKey('core.HRIncident', on_delete=models.SET_NULL, null=True, blank=True, related_name='updates')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='hr_incident_updates')
    datetime_created = DateTimeField(auto_now_add=True)

    # Document FK for attachment (single source of truth)
    attachment_document = models.ForeignKey(
        'core.Document',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='attachment_for_hr_incident_updates'
    )

    @property
    def has_attachment(self):
        """Check if update has attachment file."""
        return self.attachment_document is not None and self.attachment_document.has_file

    def get_attachment_url(self):
        """Get download URL for attachment file."""
        if self.attachment_document:
            return self.attachment_document.get_file_url()
        return None

    def get_attachment_filename(self):
        """Get filename."""
        if self.attachment_document:
            return self.attachment_document.get_filename()
        return None

    def get_attachment_size(self):
        """Get file size."""
        if self.attachment_document:
            return self.attachment_document.get_file_size()
        return None

    def __str__(self) -> str:
        return f"Update on {self.hr_incident} by {self.created_by} at {self.datetime_created}"

    class Meta:
        ordering = ['datetime_created', 'id']
        verbose_name = "HR Incident Update"
        verbose_name_plural = "HR Incident Updates"
