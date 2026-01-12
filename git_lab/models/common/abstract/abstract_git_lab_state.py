from django.db import models


class AbstractGitLabState(models.Model):
    state: str | None = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
