from django.db import models

from core.models.common.abstract.abstract_acronym import AbstractAcronym
from core.models.common.abstract.abstract_alias import AbstractAlias
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.abstract.abstract_pronunciation import AbstractPronunciation
from core.models.common.abstract.abstract_supporting_link import AbstractSupportingLink
from core.utilities.get_name_acronym import get_name_acronym


class Acronym(
    AbstractAcronym,
    AbstractAlias,
    AbstractBaseModel,
    AbstractComment,
    AbstractName,
    AbstractPronunciation,
    AbstractSupportingLink,
):
    term = models.OneToOneField(
        'Term',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='acronym'
    )

    def __str__(self):
        return get_name_acronym(acronym=self.acronym, name=self.name)

    class Meta:
        ordering = ['name', 'acronym', '-id']
