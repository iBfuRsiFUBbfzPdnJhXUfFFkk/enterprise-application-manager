from django.db.models import Model

from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class Acronym(Model):
    acronym = create_generic_varchar()

    class Meta:
        abstract = True
