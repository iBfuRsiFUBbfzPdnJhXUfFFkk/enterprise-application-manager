from django.db import models


class AbstractGitLabWebUrl(models.Model):
    web_url: str | None = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
