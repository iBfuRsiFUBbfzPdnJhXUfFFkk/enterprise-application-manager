from django.conf import settings
from django.db import models
from django.db.models import DateTimeField

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.document import Document

class BadInteractionUpdate(AbstractBaseModel, AbstractComment):
    bad_interaction = models.ForeignKey('core.BadInteraction', on_delete=models.SET_NULL, null=True, blank=True, related_name='updates')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='bad_interaction_updates')
    datetime_created = DateTimeField(auto_now_add=True)

    # MinIO file storage
    attachment_file = models.FileField(
        upload_to='bad_interactions/updates/',
        null=True,
        blank=True,
        help_text='Attachment file stored in MinIO object storage'
    )

    # Many-to-many relationship to manually link documents
    documents = models.ManyToManyField(Document, blank=True, related_name='bad_interaction_updates')

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
        return f"Update on {self.bad_interaction} by {self.created_by} at {self.datetime_created}"

    class Meta:
        ordering = ['datetime_created', 'id']
        verbose_name = "Bad Interaction Update"
        verbose_name_plural = "Bad Interaction Updates"
