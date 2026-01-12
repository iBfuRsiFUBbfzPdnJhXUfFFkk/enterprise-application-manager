from datetime import datetime

from django.db import models


class AbstractGitLabUpdatedAt(models.Model):
    updated_at: datetime | None = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
