from django.db import models


class AbstractAlias(models.Model):
    aliases_csv: str | None = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
