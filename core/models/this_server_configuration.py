from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.field_factories.create_generic_fk import create_generic_fk
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar
from core.models.role import Role
from core.models.secret import Secret


class ThisServerConfiguration(BaseModel, Comment, Name):
    connection_gitlab_api_version = create_generic_varchar()
    connection_gitlab_group_id = create_generic_varchar()
    connection_gitlab_hostname = create_generic_varchar()
    connection_gitlab_token = create_generic_fk(to=Secret)
    type_developer_role = create_generic_fk(to=Role)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']
