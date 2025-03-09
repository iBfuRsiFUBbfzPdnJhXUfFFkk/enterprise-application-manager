from django.db.models import Model

from core.models.common.field_factories.create_generic_integer import create_generic_integer


class AbstractGitLabInternalIdentification(Model):
    iid: int | None = create_generic_integer()

    class Meta:
        abstract = True
