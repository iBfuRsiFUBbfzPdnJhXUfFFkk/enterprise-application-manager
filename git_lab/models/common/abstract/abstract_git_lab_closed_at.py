from datetime import datetime

from django.db import models


class AbstractGitLabClosedAt(models.Model):
    closed_at: datetime | None = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
