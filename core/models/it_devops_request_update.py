from django.db.models import DateTimeField
from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment

class ITDevOpsRequestUpdate(AbstractBaseModel, AbstractComment):
    # Related request
    it_devops_request = models.ForeignKey("ITDevOpsRequest", on_delete=models.SET_NULL, null=True, blank=True, related_name="updates")

    # Author
    person_author = models.ForeignKey("Person", on_delete=models.SET_NULL, null=True, blank=True, related_name="it_devops_request_updates_authored")

    # Metadata
    datetime_created = DateTimeField(auto_now_add=True)
    is_internal_note = models.BooleanField(null=True, blank=True, default=False)

    # Attachments
    documents = models.ManyToManyField("Document", blank=True, related_name="it_devops_request_updates")

    def __str__(self):
        if self.it_devops_request and self.person_author:
            return f"Update by {self.person_author} on {self.it_devops_request.document_id or 'Request'}"
        elif self.person_author:
            return f"Update by {self.person_author}"
        else:
            return "Update"

    class Meta:
        ordering = ["datetime_created", "id"]
