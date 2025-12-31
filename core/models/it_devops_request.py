from django.db.models import CharField
from django_generic_model_fields.create_generic_date import create_generic_date
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_m2m import create_generic_m2m
from django_generic_model_fields.create_generic_text import create_generic_text
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.enums.it_devops_request_status_choices import IT_DEVOPS_REQUEST_STATUS_CHOICES
from core.models.common.enums.priority_choices import PRIORITY_CHOICES


class ITDevOpsRequest(AbstractBaseModel, AbstractComment, AbstractName):
    # Unique document identifier (auto-generated on save)
    document_id = CharField(max_length=255, unique=True, editable=False, blank=True, null=True)

    # Status and priority
    status = create_generic_enum(choices=IT_DEVOPS_REQUEST_STATUS_CHOICES)
    priority = create_generic_enum(choices=PRIORITY_CHOICES)

    # Details
    description = create_generic_text()
    justification = create_generic_text()
    expected_outcome = create_generic_text()
    reference_number = create_generic_varchar()

    # Dates
    date_requested = create_generic_date()
    date_due = create_generic_date()
    date_completed = create_generic_date()

    # People
    person_requester = create_generic_fk(to="Person", related_name="it_devops_requests_requested")
    person_assignee = create_generic_fk(to="Person", related_name="it_devops_requests_assigned")
    person_approver = create_generic_fk(to="Person", related_name="it_devops_requests_approved")

    # Related entities
    application = create_generic_fk(to="Application", related_name="it_devops_requests")
    project = create_generic_fk(to="Project", related_name="it_devops_requests")

    # Attachments
    attachments = create_generic_m2m(to="Document", related_name="it_devops_requests")

    # Links
    links = create_generic_m2m(to="Link", related_name="it_devops_requests")

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
        ordering = ["-date_requested", "-id"]
