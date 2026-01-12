from django.db import models


class AbstractGitLabInternalIdentification(models.Model):
    iid: int | None = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True
