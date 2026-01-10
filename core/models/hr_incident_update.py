from django.conf import settings
from django.db import models
from django.db.models import DateTimeField
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_m2m import create_generic_m2m

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.document import Document


class HRIncidentUpdate(AbstractBaseModel, AbstractComment):
    hr_incident = create_generic_fk(to='core.HRIncident', related_name='updates')
    created_by = create_generic_fk(to=settings.AUTH_USER_MODEL, related_name='hr_incident_updates')
    datetime_created = DateTimeField(auto_now_add=True)

    # MinIO file storage
    attachment_file = models.FileField(
        upload_to='hr_incidents/updates/',
        null=True,
        blank=True,
        help_text='Attachment file stored in MinIO object storage'
    )

    # Many-to-many relationship to manually link documents
    documents = create_generic_m2m(related_name='hr_incident_updates', to=Document)

    @property
    def has_attachment(self):
        """Check if update has attachment file."""
        return bool(self.attachment_file)

    def get_attachment_url(self):
        """Get download URL for attachment file."""
        if self.attachment_file:
            return self.attachment_file.url
        return None

    def get_attachment_filename(self):
        """Get filename."""
        if self.attachment_file:
            return self.attachment_file.name.split('/')[-1]
        return None

    def get_attachment_size(self):
        """Get file size."""
        if self.attachment_file:
            return self.attachment_file.size
        return None

    def __str__(self) -> str:
        return f"Update on {self.hr_incident} by {self.created_by} at {self.datetime_created}"

    class Meta:
        ordering = ['datetime_created', 'id']
        verbose_name = "HR Incident Update"
        verbose_name_plural = "HR Incident Updates"
