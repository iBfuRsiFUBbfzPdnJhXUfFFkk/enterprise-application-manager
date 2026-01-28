import hashlib

from django.db import models
from django.utils import timezone

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.abstract.abstract_version import AbstractVersion
from core.utilities.strip_exif import strip_exif_from_file
from core.utilities.uuid_upload_path import uuid_upload_path


class Document(AbstractBaseModel, AbstractComment, AbstractName, AbstractVersion):
    # MinIO file storage - uses UUID filenames to prevent collisions
    file = models.FileField(
        upload_to=uuid_upload_path,
        null=True,
        blank=True,
        help_text='File stored in MinIO object storage'
    )
    uploaded_at = models.DateTimeField(default=timezone.now, help_text='When the document was uploaded')
    file_hash = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        db_index=True,
        help_text='SHA-256 hash of file contents for duplicate detection'
    )

    def _calculate_file_hash(self):
        """Calculate SHA-256 hash of file contents."""
        if not self.file:
            return None
        try:
            self.file.seek(0)
            sha256 = hashlib.sha256()
            for chunk in self.file.chunks():
                sha256.update(chunk)
            self.file.seek(0)
            return sha256.hexdigest()
        except Exception:
            return None

    def save(self, *args, **kwargs):
        # Strip EXIF data from images before saving
        if self.file and hasattr(self.file, 'seek'):
            self.file = strip_exif_from_file(self.file)
            # Calculate hash after EXIF stripping
            self.file_hash = self._calculate_file_hash()
        super().save(*args, **kwargs)

    def get_duplicates(self):
        """Find other documents with the same file hash."""
        if not self.file_hash:
            return Document.objects.none()
        return Document.objects.filter(file_hash=self.file_hash).exclude(pk=self.pk)

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
            try:
                return self.file.size
            except Exception:
                return None
        return None

    def get_content_type(self):
        """Get file content type based on extension."""
        import mimetypes
        if self.file:
            filename = self.get_filename()
            if filename:
                content_type, _ = mimetypes.guess_type(filename)
                return content_type
        return None

    def get_file_extension(self):
        """Get file extension."""
        if self.file:
            filename = self.get_filename()
            if filename and '.' in filename:
                return filename.rsplit('.', 1)[-1].upper()
        return None

    def __str__(self):
        return f"{self.name} v{self.version}"

    class Meta:
        ordering = ['-uploaded_at', '-id']
