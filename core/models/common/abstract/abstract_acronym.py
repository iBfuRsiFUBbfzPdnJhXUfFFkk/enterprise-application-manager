from django.db import models


class AbstractAcronym(models.Model):
    acronym: str | None = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
