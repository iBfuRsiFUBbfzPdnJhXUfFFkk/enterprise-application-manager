from django.db.models import DateTimeField
from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment


class ApprovalUpdate(AbstractBaseModel, AbstractComment):
    """Model for timeline updates on approvals."""

    approval = models.ForeignKey(
        "Approval",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="updates",
    )

    person_author = models.ForeignKey(
        "Person",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approval_updates_authored",
    )

    datetime_created = DateTimeField(auto_now_add=True)
    is_internal_note = models.BooleanField(null=True, blank=True, default=False)

    documents = models.ManyToManyField(
        "Document", blank=True, related_name="approval_updates"
    )

    def __str__(self):
        if self.approval and self.person_author:
            doc_id = self.approval.document_id or "Approval"
            return f"Update by {self.person_author} on {doc_id}"
        elif self.person_author:
            return f"Update by {self.person_author}"
        return "Update"

    class Meta:
        ordering = ["datetime_created", "id"]
