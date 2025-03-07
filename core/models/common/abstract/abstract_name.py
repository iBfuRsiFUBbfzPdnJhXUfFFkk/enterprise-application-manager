from django.db.models import Model

from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class AbstractName(Model):
    name: str | None = create_generic_varchar()

    class Meta:
        abstract = True
