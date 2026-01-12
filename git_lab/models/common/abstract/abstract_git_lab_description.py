from django.db import models


class AbstractGitLabDescription(models.Model):
    description: str | None = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
