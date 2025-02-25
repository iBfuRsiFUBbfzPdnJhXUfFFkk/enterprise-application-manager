from django.db.models import CharField
from django.db.models.fields import DateField

from core.models.common.comment import Comment


class ReleaseBundle(Comment):
    bundle_name = CharField(blank=True, max_length=255, null=True)
    date_code_freeze = DateField(blank=True, null=True)
    date_demo = DateField(blank=True, null=True)
    date_release = DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.bundle_name}"
