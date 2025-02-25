from django.db.models import TextField


def create_generic_text() -> TextField:
    return TextField(blank=True, null=True)
