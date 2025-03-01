from uuid import uuid4

from django.db.models.fields import UUIDField


def create_generic_uuid() -> UUIDField:
    return UUIDField(blank=True, default=uuid4, null=True)
