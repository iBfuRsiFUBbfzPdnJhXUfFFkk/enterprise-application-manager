from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.enums.it_devops_request_status_choices import IT_DEVOPS_REQUEST_STATUS_CHOICES
from core.models.common.enums.priority_choices import PRIORITY_CHOICES


class ITDevOpsRequest(AbstractBaseModel, AbstractComment, AbstractName):
    # Unique document identifier (auto-generated on save)
    document_id = models.CharField(max_length=255, unique=True, editable=False, blank=True, null=True)

    # Status and priority
    status = models.CharField(max_length=255, choices=IT_DEVOPS_REQUEST_STATUS_CHOICES, null=True, blank=True)
    priority = models.CharField(max_length=255, choices=PRIORITY_CHOICES, null=True, blank=True)

    # Details
    description = models.TextField(null=True, blank=True)
    justification = models.TextField(null=True, blank=True)
    expected_outcome = models.TextField(null=True, blank=True)
    reference_number = models.CharField(max_length=255, null=True, blank=True)

    # Dates
    date_requested = models.DateField(null=True, blank=True)
    date_due = models.DateField(null=True, blank=True)
    date_completed = models.DateField(null=True, blank=True)

    # People
    person_requester = models.ForeignKey("Person", on_delete=models.SET_NULL, null=True, blank=True, related_name="it_devops_requests_requested")
    person_assignee = models.ForeignKey("Person", on_delete=models.SET_NULL, null=True, blank=True, related_name="it_devops_requests_assigned")
    person_approver = models.ForeignKey("Person", on_delete=models.SET_NULL, null=True, blank=True, related_name="it_devops_requests_approved")

    # Related entities
    application = models.ForeignKey("Application", on_delete=models.SET_NULL, null=True, blank=True, related_name="it_devops_requests")
    project = models.ForeignKey("Project", on_delete=models.SET_NULL, null=True, blank=True, related_name="it_devops_requests")

    # Attachments
    attachments = models.ManyToManyField("Document", blank=True, related_name="it_devops_requests")

    # Links
    links = models.ManyToManyField("Link", blank=True, related_name="it_devops_requests")

    def save(self, *args, **kwargs):
        if not self.document_id:
            # Get the highest existing document_id number
            last_request = ITDevOpsRequest.objects.order_by("-id").first()
            if last_request and last_request.document_id:
                # Extract number from format "ITREQ-00001"
                try:
                    last_num = int(last_request.document_id.split("-")[1])
                    new_num = last_num + 1
                except (IndexError, ValueError):
                    new_num = 1
            else:
                new_num = 1
            self.document_id = f"ITREQ-{new_num:05d}"
        super().save(*args, **kwargs)

    def __str__(self):
        if self.document_id and self.name:
            return f"{self.document_id}: {self.name}"
        elif self.document_id:
            return self.document_id
        elif self.name:
            return self.name
        else:
            return "Untitled Request"

    class Meta:
        ordering = ["-id"]  # Newest first (by creation order)
