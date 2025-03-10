from django.db.models import Model

from django_generic_model_fields.create_generic_text import create_generic_text


class AbstractSupportingLink(Model):
    supporting_links_csv: str | None = create_generic_text()

    class Meta:
        abstract = True
