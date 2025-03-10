from datetime import datetime

from django.db.models import Model

from django_generic_model_fields.create_generic_datetime import create_generic_datetime


class AbstractGitLabCreatedAt(Model):
    created_at: datetime | None = create_generic_datetime()

    class Meta:
        abstract = True
