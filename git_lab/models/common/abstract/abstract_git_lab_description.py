from django.db.models import Model

from django_generic_model_fields.create_generic_text import create_generic_text


class AbstractGitLabDescription(Model):
    description: str | None = create_generic_text()

    class Meta:
        abstract = True
