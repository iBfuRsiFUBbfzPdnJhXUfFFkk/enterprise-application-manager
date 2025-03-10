from django.db.models import Model

from django_generic_model_fields.create_generic_varchar import create_generic_varchar


class AbstractPronunciation(Model):
    pronunciation: str | None = create_generic_varchar()

    class Meta:
        abstract = True
