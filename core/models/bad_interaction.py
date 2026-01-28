from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.enums.bad_interaction_severity_choices import BAD_INTERACTION_SEVERITY_CHOICES


class BadInteraction(AbstractBaseModel, AbstractComment):
    name = models.CharField(max_length=255, null=True, blank=True, help_text='Brief title for the interaction')
    person = models.ForeignKey('core.Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='bad_interactions')
    reported_by = models.ForeignKey('core.Person', on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_bad_interactions')
    date_occurred = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True, help_text='Description of what happened')
    severity = models.CharField(max_length=255, choices=BAD_INTERACTION_SEVERITY_CHOICES, null=True, blank=True)

    # Document FK for evidence file (single source of truth)
    evidence_document = models.ForeignKey(
        'core.Document',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evidence_for_bad_interactions'
    )

    @property
    def has_evidence(self):
        """Check if bad interaction has evidence file."""
        return self.evidence_document is not None and self.evidence_document.has_file

    @property
    def evidence_file_exists(self):
        """Check if evidence file actually exists in storage."""
        if not self.evidence_document or not self.evidence_document.file:
            return False
        try:
            return self.evidence_document.file.storage.exists(self.evidence_document.file.name)
        except Exception:
            return False

    def get_evidence_url(self):
        """Get download URL for evidence file."""
        if self.evidence_document:
            return self.evidence_document.get_file_url()
        return None

    def get_evidence_filename(self):
        """Get filename."""
        if self.evidence_document:
            return self.evidence_document.get_filename()
        return None

    def get_evidence_size(self):
        """Get file size."""
        if self.evidence_document:
            return self.evidence_document.get_file_size()
        return None

    @property
    def is_evidence_image(self) -> bool:
        """Check if evidence file is an image."""
        if not self.evidence_document or not self.evidence_document.file:
            return False
        filename = self.evidence_document.file.name.lower()
        return filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg'))

    @property
    def is_evidence_pdf(self) -> bool:
        """Check if evidence file is a PDF."""
        if not self.evidence_document or not self.evidence_document.file:
            return False
        return self.evidence_document.file.name.lower().endswith('.pdf')

    @property
    def evidence_file_type(self) -> str:
        """Get the type of evidence file."""
        if not self.evidence_document or not self.evidence_document.file:
            return 'none'
        filename = self.evidence_document.file.name.lower()
        if filename.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.svg')):
            return 'image'
        elif filename.endswith('.pdf'):
            return 'pdf'
        elif filename.endswith(('.doc', '.docx')):
            return 'word'
        elif filename.endswith(('.xls', '.xlsx')):
            return 'excel'
        elif filename.endswith(('.txt', '.csv', '.json', '.xml')):
            return 'text'
        return 'other'

    def __str__(self) -> str:
        if self.name:
            return self.name
        return f"BadInteraction - {self.person} on {self.date_occurred}"

    class Meta:
        ordering = ['-date_occurred', 'id']
        verbose_name = "Bad Interaction"
        verbose_name_plural = "Bad Interactions"
