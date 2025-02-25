from django.db.models import CharField


def create_generic_varchar() -> CharField:
    return CharField(blank=True, max_length=255, null=True)
