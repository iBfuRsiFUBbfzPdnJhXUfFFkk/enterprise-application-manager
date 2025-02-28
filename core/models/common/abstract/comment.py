from django.db.models import Model

from core.models.common.field_factories.create_generic_text import create_generic_text


class Comment(Model):
    comment = create_generic_text()

    class Meta:
        abstract = True
