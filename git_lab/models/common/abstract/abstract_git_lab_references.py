from django.db.models import Model

from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class AbstractGitLabReferences(Model):
    references_long: str | None = create_generic_varchar()
    references_relative: str | None = create_generic_varchar()
    references_short: str | None = create_generic_varchar()

    class Meta:
        abstract = True
