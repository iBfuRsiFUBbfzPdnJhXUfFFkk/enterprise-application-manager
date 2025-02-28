from django.db.models import ForeignKey, Model, DO_NOTHING


def create_generic_fk(
        related_name: str,
        to: type[Model],
) -> ForeignKey:
    return ForeignKey(
        blank=True,
        null=True,
        on_delete=DO_NOTHING,
        related_name=related_name,
        to=to,
    )
