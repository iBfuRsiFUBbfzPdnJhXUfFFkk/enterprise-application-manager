from django.db.models import IntegerField


def create_generic_integer() -> IntegerField:
    return IntegerField(blank=True, null=True)
