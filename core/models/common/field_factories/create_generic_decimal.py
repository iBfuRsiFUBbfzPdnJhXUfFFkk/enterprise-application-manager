from django.db.models import DecimalField


def create_generic_decimal() -> DecimalField:
    return DecimalField(
        blank=True,
        decimal_places=7,
        max_digits=20,
        null=True,
    )
