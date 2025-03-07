from django.db.models import Model, DO_NOTHING, OneToOneField


def create_generic_one_to_one_fk(
        related_name: str | None = None,
        to: type[Model] | str | None = None,
) -> OneToOneField:
    return OneToOneField(
        blank=True,
        null=True,
        on_delete=DO_NOTHING,
        related_name=related_name,
        to=to,
    )
