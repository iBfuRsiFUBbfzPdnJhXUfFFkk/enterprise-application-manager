from django.db.models import DateTimeField
from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_fk import create_generic_fk

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment


class ITDevOpsRequestUpdate(AbstractBaseModel, AbstractComment):
    # Related request
    it_devops_request = create_generic_fk(to="ITDevOpsRequest", related_name="updates")

    # Author
    person_author = create_generic_fk(to="Person", related_name="it_devops_request_updates_authored")

    # Metadata
    datetime_created = DateTimeField(auto_now_add=True)
    is_internal_note = create_generic_boolean(default=False)

    def __str__(self):
        if self.it_devops_request and self.person_author:
            return f"Update by {self.person_author} on {self.it_devops_request.document_id or 'Request'}"
        elif self.person_author:
            return f"Update by {self.person_author}"
        else:
            return "Update"

    class Meta:
        ordering = ["datetime_created", "id"]
