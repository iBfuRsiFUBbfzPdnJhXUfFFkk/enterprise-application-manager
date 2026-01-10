from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.abstract.abstract_version import AbstractVersion


class Document(AbstractBaseModel, AbstractComment, AbstractName, AbstractVersion):
    # MinIO file storage
    file = models.FileField(
        upload_to='documents/',
        null=True,
        blank=True,
        help_text='File stored in MinIO object storage'
    )

    @property
    def has_file(self):
        """Check if document has a file."""
        return bool(self.file)

    def get_file_url(self):
        """Get download URL for file."""
        if self.file:
            # Return authenticated Django view URL instead of direct S3 URL
            from django.urls import reverse
            return reverse('document_file', kwargs={'model_id': self.pk})
        return None

    def get_filename(self):
        """Get filename."""
        if self.file:
            return self.file.name.split('/')[-1]
        return None

    def get_file_size(self):
        """Get file size."""
        if self.file:
            return self.file.size
        return None

    def __str__(self):
        return f"{self.name} v{self.version}"

    class Meta:
        ordering = ['name', '-id']
