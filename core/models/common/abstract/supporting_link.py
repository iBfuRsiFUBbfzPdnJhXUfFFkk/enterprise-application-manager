from django.db.models import Model

from core.models.common.field_factories.create_generic_text import create_generic_text


class SupportingLink(Model):
    supporting_links_csv = create_generic_text()

    class Meta:
        abstract = True
