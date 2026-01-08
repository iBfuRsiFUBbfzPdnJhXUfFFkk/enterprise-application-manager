from django.db import models
from django_generic_model_fields.create_generic_blob import create_generic_blob
from django_generic_model_fields.create_generic_date import create_generic_date
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.enums.bad_interaction_severity_choices import BAD_INTERACTION_SEVERITY_CHOICES


class BadInteraction(AbstractBaseModel, AbstractComment):
    person = create_generic_fk(to='core.Person', related_name='bad_interactions')
    reported_by = create_generic_fk(to='core.Person', related_name='reported_bad_interactions')
    date_occurred = create_generic_date()
    description: str | None = models.TextField(blank=True, null=True, help_text='Description of what happened')
    evidence_blob_content_type: str | None = create_generic_varchar()
    evidence_blob_data: bytes | None = create_generic_blob()
    evidence_blob_filename: str | None = create_generic_varchar()
    evidence_blob_size: int | None = create_generic_integer()
    severity: str = create_generic_enum(choices=BAD_INTERACTION_SEVERITY_CHOICES)

    def __str__(self) -> str:
        return f"BadInteraction - {self.person} on {self.date_occurred}"

    class Meta:
        ordering = ['-date_occurred', 'id']
        verbose_name = "Bad Interaction"
        verbose_name_plural = "Bad Interactions"
