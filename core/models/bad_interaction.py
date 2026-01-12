from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.enums.bad_interaction_severity_choices import BAD_INTERACTION_SEVERITY_CHOICES
from core.models.document import Document

class BadInteraction(AbstractBaseModel, AbstractComment):
    person = models.ForeignKey('core.Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='bad_interactions')
    reported_by = models.ForeignKey('core.Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_bad_interactions')
    date_occurred = models.DateField(null=True, blank=True)
    description: str | None = models.TextField(blank=True, null=True, help_text='Description of what happened')
    severity: str = models.CharField(max_length=255, choices=BAD_INTERACTION_SEVERITY_CHOICES, null=True, blank=True)

    # MinIO file storage
    evidence_file = models.FileField(
        upload_to='bad_interactions/evidence/',
        null=True,
        blank=True,
        help_text='Evidence file stored in MinIO object storage'
    )

    # Many-to-many relationship to manually link documents
    documents = models.ManyToManyField(Document, blank=True, related_name='bad_interactions')

    @property
    def has_evidence(self):
        """Check if bad interaction has evidence file."""
        return bool(self.evidence_file)

    def get_evidence_url(self):
        """Get download URL for evidence file."""
        if self.evidence_file:
            return self.evidence_file.url
        return None

    def get_evidence_filename(self):
        """Get filename."""
        if self.evidence_file:
            return self.evidence_file.name.split('/')[-1]
        return None

    def get_evidence_size(self):
        """Get file size."""
        if self.evidence_file:
            return self.evidence_file.size
        return None

    def __str__(self) -> str:
        return f"BadInteraction - {self.person} on {self.date_occurred}"

    class Meta:
        ordering = ['-date_occurred', 'id']
        verbose_name = "Bad Interaction"
        verbose_name_plural = "Bad Interactions"
