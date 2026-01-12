from django.db import models


class AbstractVersion(models.Model):
    version: str | None = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
