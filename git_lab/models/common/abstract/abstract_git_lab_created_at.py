from datetime import datetime

from django.db import models


class AbstractGitLabCreatedAt(models.Model):
    created_at: datetime | None = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
