from django.db.models import DateField


def create_generic_date() -> DateField:
    return DateField(blank=True, null=True)
