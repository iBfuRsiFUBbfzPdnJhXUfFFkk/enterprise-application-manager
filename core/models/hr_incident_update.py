from django.conf import settings
from django.db.models import DateTimeField
from django_generic_model_fields.create_generic_blob import create_generic_blob
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment


class HRIncidentUpdate(AbstractBaseModel, AbstractComment):
    hr_incident = create_generic_fk(to='core.HRIncident', related_name='updates')
    created_by = create_generic_fk(to=settings.AUTH_USER_MODEL, related_name='hr_incident_updates')
    datetime_created = DateTimeField(auto_now_add=True)
    attachment_blob_content_type: str | None = create_generic_varchar()
    attachment_blob_data: bytes | None = create_generic_blob()
    attachment_blob_filename: str | None = create_generic_varchar()
    attachment_blob_size: int | None = create_generic_integer()

    def __str__(self) -> str:
        return f"Update on {self.hr_incident} by {self.created_by} at {self.datetime_created}"

    class Meta:
        ordering = ['datetime_created', 'id']
        verbose_name = "HR Incident Update"
        verbose_name_plural = "HR Incident Updates"
