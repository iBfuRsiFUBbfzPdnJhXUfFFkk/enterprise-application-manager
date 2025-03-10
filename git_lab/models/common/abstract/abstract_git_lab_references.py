from django.db.models import Model

from django_generic_model_fields.create_generic_varchar import create_generic_varchar


class AbstractGitLabReferences(Model):
    references_long: str | None = create_generic_varchar()
    references_relative: str | None = create_generic_varchar()
    references_short: str | None = create_generic_varchar()

    class Meta:
        abstract = True
