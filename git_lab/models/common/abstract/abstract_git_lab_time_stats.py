from django.db.models import Model

from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_varchar import create_generic_varchar


class AbstractGitLabTimeStats(Model):
    time_stats_human_time_estimate: str | None = create_generic_varchar()
    time_stats_human_total_time_spent: str | None = create_generic_varchar()
    time_stats_time_estimate: int | None = create_generic_integer()
    time_stats_total_time_spent: int | None = create_generic_integer()

    class Meta:
        abstract = True
