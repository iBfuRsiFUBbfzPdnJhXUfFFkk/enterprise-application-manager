from django.core.exceptions import ValidationError
from django_generic_model_fields.create_generic_boolean import create_generic_boolean

from core.models.common.abstract.abstract_acronym import AbstractAcronym
from core.models.common.abstract.abstract_alias import AbstractAlias
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.utilities.cast_query_set import cast_query_set
from core.utilities.get_name_acronym import get_name_acronym


class Role(
    AbstractAcronym,
    AbstractAlias,
    AbstractBaseModel,
    AbstractComment,
    AbstractName,
):
    is_protected: bool | None = create_generic_boolean(default=False)

    @property
    def people_who_hold_this_role(self):
        from core.models.person import Person
        return cast_query_set(
            typ=Person,
            val=Person.objects.filter(roles=self)
        )

    def delete(self, *args, **kwargs):
        """
        Override delete to prevent deletion of protected roles.
        Protected roles are essential to the application and cannot be removed.
        """
        if self.is_protected:
            raise ValidationError(
                f"Cannot delete protected role '{self.name}'. "
                f"This role is required by the application and cannot be removed."
            )
        return super().delete(*args, **kwargs)

    def __str__(self) -> str:
        return get_name_acronym(acronym=self.acronym, name=self.name)

    class Meta:
        ordering = ['name', '-id']
        verbose_name = "Role"
        verbose_name_plural = "Roles"
