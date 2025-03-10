from django.db.models import Model

from django_generic_model_fields.create_generic_integer import create_generic_integer


class AbstractGitLabInternalIdentification(Model):
    iid: int | None = create_generic_integer()

    class Meta:
        abstract = True
