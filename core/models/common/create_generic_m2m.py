from django.db.models import Model, ManyToManyField


def create_generic_m2m(
        to: type[Model] | str,
) -> ManyToManyField:
    return ManyToManyField(
        blank=True,
        to=to,
    )
