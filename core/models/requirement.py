from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.field_factories.create_generic_boolean import create_generic_boolean


class Requirement(Comment, Name):
    is_for_soc = create_generic_boolean()
    is_for_spsrd = create_generic_boolean()
    is_functional_requirement = create_generic_boolean()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
