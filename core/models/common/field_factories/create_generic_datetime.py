from django.db.models import DateTimeField


def create_generic_datetime() -> DateTimeField:
    return DateTimeField(blank=True, null=True)
