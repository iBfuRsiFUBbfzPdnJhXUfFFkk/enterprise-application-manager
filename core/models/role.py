from typing import cast

from django.db.models import QuerySet

from core.models.common.abstract.acronym import Acronym
from core.models.common.abstract.alias import Alias
from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.utilities.get_name_acronym import get_name_acronym


class Role(Acronym, Alias, BaseModel, Comment, Name):
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
