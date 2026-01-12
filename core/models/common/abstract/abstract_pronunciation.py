from django.db import models


class AbstractPronunciation(models.Model):
    pronunciation: str | None = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        abstract = True
