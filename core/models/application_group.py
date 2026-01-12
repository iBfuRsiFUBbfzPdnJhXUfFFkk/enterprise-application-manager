from django.db import models
from core.models.common.abstract.abstract_acronym import AbstractAcronym
from core.models.common.abstract.abstract_alias import AbstractAlias
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.enums.lifecycle_choices import LIFECYCLE_CHOICES
from core.utilities.get_name_acronym import get_name_acronym


class ApplicationGroup(AbstractAlias, AbstractAcronym, AbstractBaseModel, AbstractComment, AbstractName):
    is_externally_facing = models.BooleanField(null=True, blank=True)
    is_platform = models.BooleanField(null=True, blank=True)
    type_lifecycle = models.CharField(max_length=255, choices=LIFECYCLE_CHOICES, null=True, blank=True)

    def __str__(self):
        return get_name_acronym(acronym=self.acronym, name=self.name)

    class Meta:
        ordering = ['name', '-id']
