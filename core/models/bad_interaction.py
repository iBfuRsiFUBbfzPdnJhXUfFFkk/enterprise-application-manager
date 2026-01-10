from django.db import models
from django_generic_model_fields.create_generic_blob import create_generic_blob
from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_date import create_generic_date
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_m2m import create_generic_m2m
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.enums.bad_interaction_severity_choices import BAD_INTERACTION_SEVERITY_CHOICES
from core.models.document import Document


class BadInteraction(AbstractBaseModel, AbstractComment):
    person = create_generic_fk(to='core.Person', related_name='bad_interactions')
    reported_by = create_generic_fk(to='core.Person', related_name='reported_bad_interactions')
    date_occurred = create_generic_date()
    description: str | None = models.TextField(blank=True, null=True, help_text='Description of what happened')
    severity: str = create_generic_enum(choices=BAD_INTERACTION_SEVERITY_CHOICES)

    # Legacy blob storage (deprecated but kept for migration)
    evidence_blob_content_type: str | None = create_generic_varchar()
    evidence_blob_data: bytes | None = create_generic_blob()
    evidence_blob_filename: str | None = create_generic_varchar()
    evidence_blob_size: int | None = create_generic_integer()

    # New MinIO file storage
    evidence_file = models.FileField(
        upload_to='bad_interactions/evidence/',
        null=True,
        blank=True,
        help_text='Evidence file stored in MinIO object storage'
    )

    # Migration tracking flag
    migrated_to_minio = create_generic_boolean(default=False)

    # Many-to-many relationship to manually link documents
    documents = create_generic_m2m(related_name='bad_interactions', to=Document)

    @property
    def has_evidence(self):
        """Check if bad interaction has evidence file in either storage."""
        return bool(self.evidence_file) or bool(self.evidence_blob_data)

    def get_evidence_url(self):
        """Get download URL for evidence file (handles both storage types)."""
        if self.evidence_file:
            return self.evidence_file.url
        elif self.evidence_blob_data:
            # Legacy blob download view
            from django.urls import reverse
            return reverse('bad_interaction_download_evidence', kwargs={'pk': self.pk})
        return None

    def get_evidence_filename(self):
        """Get filename from either storage."""
        if self.evidence_file:
            return self.evidence_file.name.split('/')[-1]
        return self.evidence_blob_filename

    def get_evidence_size(self):
        """Get file size from either storage."""
        if self.evidence_file:
            return self.evidence_file.size
        return self.evidence_blob_size

    def __str__(self) -> str:
        return f"BadInteraction - {self.person} on {self.date_occurred}"

    class Meta:
        ordering = ['-date_occurred', 'id']
        verbose_name = "Bad Interaction"
        verbose_name_plural = "Bad Interactions"
