from django.db import models


class AbstractGitLabTitle(models.Model):
    title: str | None = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
