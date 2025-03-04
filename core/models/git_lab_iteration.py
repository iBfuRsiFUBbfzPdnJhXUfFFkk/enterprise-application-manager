from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.field_factories.create_generic_fk import create_generic_fk
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class GitLabIteration(BaseModel, Comment, Name):
    git_lab_id = create_generic_varchar()
    sprint = create_generic_fk(related_name="git_lab_iterations", to='Sprint')

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['-id']
