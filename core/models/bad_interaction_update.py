from django.conf import settings
from django.db import models
from django.db.models import DateTimeField
from django_generic_model_fields.create_generic_blob import create_generic_blob
from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_m2m import create_generic_m2m
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.document import Document


class BadInteractionUpdate(AbstractBaseModel, AbstractComment):
    bad_interaction = create_generic_fk(to='core.BadInteraction', related_name='updates')
    created_by = create_generic_fk(to=settings.AUTH_USER_MODEL, related_name='bad_interaction_updates')
    datetime_created = DateTimeField(auto_now_add=True)

    # Legacy blob storage (deprecated but kept for migration)
    attachment_blob_content_type: str | None = create_generic_varchar()
    attachment_blob_data: bytes | None = create_generic_blob()
    attachment_blob_filename: str | None = create_generic_varchar()
    attachment_blob_size: int | None = create_generic_integer()

    # New MinIO file storage
    attachment_file = models.FileField(
        upload_to='bad_interactions/updates/',
        null=True,
        blank=True,
        help_text='Attachment file stored in MinIO object storage'
    )

    # Migration tracking flag
    migrated_to_minio = create_generic_boolean(default=False)

    # Many-to-many relationship to manually link documents
    documents = create_generic_m2m(related_name='bad_interaction_updates', to=Document)

    @property
    def has_attachment(self):
        """Check if update has attachment file in either storage."""
        return bool(self.attachment_file) or bool(self.attachment_blob_data)

    def get_attachment_url(self):
        """Get download URL for attachment file (handles both storage types)."""
        if self.attachment_file:
            return self.attachment_file.url
        elif self.attachment_blob_data:
            # Legacy blob download view
            from django.urls import reverse
            return reverse('bad_interaction_download_update_attachment', kwargs={'update_id': self.pk})
        return None

    def get_attachment_filename(self):
        """Get filename from either storage."""
        if self.attachment_file:
            return self.attachment_file.name.split('/')[-1]
        return self.attachment_blob_filename

    def get_attachment_size(self):
        """Get file size from either storage."""
        if self.attachment_file:
            return self.attachment_file.size
        return self.attachment_blob_size

    def __str__(self) -> str:
        return f"Update on {self.bad_interaction} by {self.created_by} at {self.datetime_created}"

    class Meta:
        ordering = ['datetime_created', 'id']
        verbose_name = "Bad Interaction Update"
        verbose_name_plural = "Bad Interaction Updates"
