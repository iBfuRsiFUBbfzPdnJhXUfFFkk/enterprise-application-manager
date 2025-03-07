from typing import cast

from django.db.models import QuerySet

from core.models.common.abstract.abstract_acronym import AbstractAcronym
from core.models.common.abstract.abstract_alias import AbstractAlias
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.utilities.get_name_acronym import get_name_acronym


class Role(AbstractAcronym, AbstractAlias, AbstractBaseModel, AbstractComment, AbstractName):
    @property
    def get_people_who_hold_this_role(self) -> QuerySet:
        from core.models.person import Person
        return cast(
            typ=QuerySet[Person],
            val=Person.objects.filter(roles=self)
        )

    def __str__(self):
        return get_name_acronym(acronym=self.acronym, name=self.name)

    class Meta:
        ordering = ['name', '-id']
