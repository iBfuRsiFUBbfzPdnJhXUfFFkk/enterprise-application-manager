from datetime import date

from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.enums.approval_status_choices import APPROVAL_STATUS_CHOICES


class Approval(AbstractBaseModel, AbstractComment, AbstractName):
    """Model for recording historical approvals."""

    document_id = models.CharField(
        max_length=255, unique=True, editable=False, blank=True, null=True
    )

    status = models.CharField(
        max_length=255, choices=APPROVAL_STATUS_CHOICES, null=True, blank=True
    )

    description = models.TextField(null=True, blank=True)

    application = models.ForeignKey(
        "Application",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approvals",
    )

    project = models.ForeignKey(
        "Project",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approvals",
    )

    person_requester = models.ForeignKey(
        "Person",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approvals_requested",
    )

    approvers = models.ManyToManyField(
        "Person",
        blank=True,
        related_name="approvals_approved",
    )

    date_requested = models.DateField(null=True, blank=True)
    date_approved = models.DateField(null=True, blank=True)
    date_expiration = models.DateField(null=True, blank=True)

    documents = models.ManyToManyField(
        "Document", blank=True, related_name="approvals"
    )

    links = models.ManyToManyField("Link", blank=True, related_name="approvals")

    reference_number = models.CharField(max_length=255, null=True, blank=True)

    @property
    def is_expired(self) -> bool:
        """Check if the approval has expired based on expiration date."""
        if self.date_expiration:
            return date.today() > self.date_expiration
        return False

    def save(self, *args, **kwargs):
        if not self.document_id:
            last_approval = Approval.objects.order_by("-id").first()
            if last_approval and last_approval.document_id:
                try:
                    last_num = int(last_approval.document_id.split("-")[1])
                    new_num = last_num + 1
                except (IndexError, ValueError):
                    new_num = 1
            else:
                new_num = 1
            self.document_id = f"APPR-{new_num:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        if self.document_id and self.name:
            return f"{self.document_id}: {self.name}"
        elif self.document_id:
            return self.document_id
        elif self.name:
            return self.name
        return "Untitled Approval"

    class Meta:
        ordering = ["-id"]
