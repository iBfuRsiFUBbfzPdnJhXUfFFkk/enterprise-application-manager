from django.db import models
from django.db.models import Model


class AbstractUniformResourceLocator(Model):
    url: str | None = models.CharField(
        max_length=2000,
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
