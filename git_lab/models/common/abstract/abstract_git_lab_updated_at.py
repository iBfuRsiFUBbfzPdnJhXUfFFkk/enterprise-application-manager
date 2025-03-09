from datetime import datetime

from django.db.models import Model

from core.models.common.field_factories.create_generic_datetime import create_generic_datetime


class AbstractGitLabUpdatedAt(Model):
    updated_at: datetime | None = create_generic_datetime()

    class Meta:
        abstract = True
