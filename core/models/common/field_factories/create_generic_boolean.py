from django.db.models import BooleanField


def create_generic_boolean(default: bool = False) -> BooleanField:
    return BooleanField(blank=True, default=default, null=True)
