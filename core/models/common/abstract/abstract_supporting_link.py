from django.db import models


class AbstractSupportingLink(models.Model):
    supporting_links_csv: str | None = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
