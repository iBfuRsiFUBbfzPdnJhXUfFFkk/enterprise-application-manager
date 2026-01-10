from django.db import models
from django_generic_model_fields.create_generic_blob import create_generic_blob
from django_generic_model_fields.create_generic_boolean import create_generic_boolean

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.abstract.abstract_version import AbstractVersion
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_varchar import create_generic_varchar


class Document(AbstractBaseModel, AbstractComment, AbstractName, AbstractVersion):
    # Legacy blob storage (deprecated but kept for migration)
    blob_content_type = create_generic_varchar()
    blob_data = create_generic_blob()
    blob_filename = create_generic_varchar()
    blob_size = create_generic_integer()

    # New MinIO file storage
    file = models.FileField(
        upload_to='documents/',
        null=True,
        blank=True,
        help_text='File stored in MinIO object storage'
    )

    # Migration tracking flag
    migrated_to_minio = create_generic_boolean(default=False)

    @property
    def has_file(self):
        """Check if document has file in either storage."""
        return bool(self.file) or bool(self.blob_data)

    def get_file_url(self):
        """Get download URL for file (handles both storage types)."""
        if self.file:
            return self.file.url
        elif self.blob_data:
            # Legacy blob download view
            from django.urls import reverse
            return reverse('document_download', kwargs={'pk': self.pk})
        return None

    def get_filename(self):
        """Get filename from either storage."""
        if self.file:
            return self.file.name.split('/')[-1]
        return self.blob_filename

    def get_file_size(self):
        """Get file size from either storage."""
        if self.file:
            return self.file.size
        return self.blob_size

    def __str__(self):
        return f"{self.name} v{self.version}"

    class Meta:
        ordering = ['name', '-id']
