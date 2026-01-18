from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class AbstractCommentable(models.Model):
    """Mixin to add comment support to any model."""

    comments = GenericRelation(
        'core.Comment',
        content_type_field='content_type',
        object_id_field='object_id',
    )

    class Meta:
        abstract = True
