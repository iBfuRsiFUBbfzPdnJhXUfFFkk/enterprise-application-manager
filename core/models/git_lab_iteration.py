from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.field_factories.create_generic_fk import create_generic_fk
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class GitLabIteration(AbstractBaseModel, AbstractComment, AbstractName):
    git_lab_id = create_generic_varchar()
    sprint = create_generic_fk(related_name="git_lab_iterations", to='Sprint')

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-id']
