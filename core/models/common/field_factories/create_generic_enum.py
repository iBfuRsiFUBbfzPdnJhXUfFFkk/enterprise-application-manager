from django.db.models import CharField


def create_generic_enum(choices: list[tuple[str, str]]) -> CharField:
    return CharField(blank=True, choices=choices, max_length=255, null=True)
