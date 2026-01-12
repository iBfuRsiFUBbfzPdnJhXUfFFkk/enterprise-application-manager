from django.db import models


class AbstractGitLabReferences(models.Model):
    references_long: str | None = models.CharField(max_length=255, null=True, blank=True)
    references_relative: str | None = models.CharField(max_length=255, null=True, blank=True)
    references_short: str | None = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
