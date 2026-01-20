from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.enums.priority_choices import PRIORITY_CHOICES
from core.models.common.enums.proposal_status_choices import PROPOSAL_STATUS_CHOICES


class Proposal(AbstractBaseModel, AbstractComment, AbstractName):
    document_id = models.CharField(
        max_length=255, unique=True, editable=False, blank=True, null=True
    )

    status = models.CharField(
        max_length=255, choices=PROPOSAL_STATUS_CHOICES, null=True, blank=True
    )
    priority = models.CharField(
        max_length=255, choices=PRIORITY_CHOICES, null=True, blank=True
    )

    # Content sections (Markdown supported)
    executive_summary = models.TextField(null=True, blank=True)
    problem_statement = models.TextField(null=True, blank=True)
    proposed_solution = models.TextField(null=True, blank=True)
    benefits = models.TextField(null=True, blank=True)
    risks_and_mitigations = models.TextField(null=True, blank=True)
    timeline = models.TextField(null=True, blank=True)
    resources_required = models.TextField(null=True, blank=True)
    success_criteria = models.TextField(null=True, blank=True)

    # People
    person_author = models.ForeignKey(
        "Person",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="proposals_authored",
    )
    person_reviewer = models.ForeignKey(
        "Person",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="proposals_reviewed",
    )
    person_approver = models.ForeignKey(
        "Person",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="proposals_approved",
    )

    # Dates
    date_created = models.DateField(null=True, blank=True)
    date_submitted = models.DateField(null=True, blank=True)
    date_review_completed = models.DateField(null=True, blank=True)
    date_decision = models.DateField(null=True, blank=True)
    date_implementation_target = models.DateField(null=True, blank=True)

    # Related entities
    application = models.ForeignKey(
        "Application",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="proposals",
    )
    project = models.ForeignKey(
        "Project",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="proposals",
    )

    # Attachments and links
    attachments = models.ManyToManyField("Document", blank=True, related_name="proposals")
    links = models.ManyToManyField("Link", blank=True, related_name="proposals")

    # Metadata
    version = models.CharField(max_length=50, null=True, blank=True)
    reference_number = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.document_id:
            last_proposal = Proposal.objects.order_by("-id").first()
            if last_proposal and last_proposal.document_id:
                try:
                    last_num = int(last_proposal.document_id.split("-")[1])
                    new_num = last_num + 1
                except (IndexError, ValueError):
                    new_num = 1
            else:
                new_num = 1
            self.document_id = f"PROP-{new_num:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        if self.document_id and self.name:
            return f"{self.document_id}: {self.name}"
        elif self.document_id:
            return self.document_id
        elif self.name:
            return self.name
        else:
            return "Untitled Proposal"

    class Meta:
        ordering = ["-date_created", "-id"]
