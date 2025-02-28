from django.db.models import BinaryField


def create_generic_blob() -> BinaryField:
    return BinaryField(blank=True, null=True)
