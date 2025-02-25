from django.db.models import Model, ManyToManyField


def create_generic_m2m(
        to: type[Model] | str,
        related_name: str | None = None,
) -> ManyToManyField:
    return ManyToManyField(
        blank=True,
        related_name=related_name,
        to=to,
    )
