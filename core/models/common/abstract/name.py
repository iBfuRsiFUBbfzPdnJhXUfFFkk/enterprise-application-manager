from django.db.models import Model

from core.models.common.field_factories.create_generic_text import create_generic_text


class Name(Model):
    name = create_generic_text()

    class Meta:
        abstract = True
