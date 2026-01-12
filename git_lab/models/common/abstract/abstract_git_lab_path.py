from django.db import models


class AbstractGitLabPath(models.Model):
    path: str | None = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
