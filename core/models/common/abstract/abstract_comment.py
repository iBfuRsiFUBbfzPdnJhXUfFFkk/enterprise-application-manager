from django.db import models


class AbstractComment(models.Model):
    comment: str | None = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
