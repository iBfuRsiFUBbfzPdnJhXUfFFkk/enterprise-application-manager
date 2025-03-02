from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.name import Name
from core.models.common.abstract.version import Version
from core.models.common.field_factories.create_generic_blob import create_generic_blob
from core.models.common.field_factories.create_generic_integer import create_generic_integer
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class Document(BaseModel, Comment, Name, Version):
    blob_content_type = create_generic_varchar()
    blob_data = create_generic_blob()
    blob_filename = create_generic_varchar()
    blob_size = create_generic_integer()

    def __str__(self):
        return f"{self.name} v{self.version}"

    class Meta:
        ordering = ['name', '-id']
