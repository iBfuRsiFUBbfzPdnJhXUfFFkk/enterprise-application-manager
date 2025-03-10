from django.db.models import Model

from django_generic_model_fields.create_generic_varchar import create_generic_varchar


class AbstractAlias(Model):
    aliases_csv: str | None = create_generic_varchar()

    class Meta:
        abstract = True
