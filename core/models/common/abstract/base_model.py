from django.db.models import Model, ForeignKey, SET_NULL
from simple_history.models import HistoricalRecords

from core.settings import AUTH_USER_MODEL


class BaseModel(Model):
    history = HistoricalRecords(inherit=True)
    history_user = ForeignKey(
        blank=True,
        null=True,
        on_delete=SET_NULL,
        to=AUTH_USER_MODEL,
    )

    class Meta:
        abstract = True
