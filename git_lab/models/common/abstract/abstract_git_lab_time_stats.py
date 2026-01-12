from django.db import models


class AbstractGitLabTimeStats(models.Model):
    time_stats_human_time_estimate: str | None = models.CharField(max_length=255, null=True, blank=True)
    time_stats_human_total_time_spent: str | None = models.CharField(max_length=255, null=True, blank=True)
    time_stats_time_estimate: int | None = models.IntegerField(null=True, blank=True)
    time_stats_total_time_spent: int | None = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True
