from django.db import models


class AbstractName(models.Model):
    name: str | None = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
