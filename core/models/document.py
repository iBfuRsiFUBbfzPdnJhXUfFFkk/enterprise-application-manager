from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.abstract.abstract_version import AbstractVersion
from core.models.common.field_factories.create_generic_blob import create_generic_blob
from core.models.common.field_factories.create_generic_integer import create_generic_integer
from core.models.common.field_factories.create_generic_varchar import create_generic_varchar


class Document(AbstractBaseModel, AbstractComment, AbstractName, AbstractVersion):
    blob_content_type = create_generic_varchar()
    blob_data = create_generic_blob()
    blob_filename = create_generic_varchar()
    blob_size = create_generic_integer()

    def __str__(self):
        return f"{self.name} v{self.version}"

    class Meta:
        ordering = ['name', '-id']
