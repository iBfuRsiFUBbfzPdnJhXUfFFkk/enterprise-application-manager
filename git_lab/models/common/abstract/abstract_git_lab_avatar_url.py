from django.db.models import Model

from django_generic_model_fields.create_generic_varchar import create_generic_varchar


class AbstractGitLabAvatarUrl(Model):
    avatar_url: str | None = create_generic_varchar()

    class Meta:
        abstract = True
