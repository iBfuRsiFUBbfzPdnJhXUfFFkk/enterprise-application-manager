from core.models.application import Application
from core.models.common.abstract.base_model import BaseModel
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.version import Version
from core.models.common.enums.sign_off_choices import SIGN_OFF_CHOICES
from core.models.common.field_factories.create_generic_enum import create_generic_enum
from core.models.common.field_factories.create_generic_fk import create_generic_fk
from core.models.release_bundle import ReleaseBundle


class Release(BaseModel, Comment, Version):
    application = create_generic_fk(related_name='releases', to=Application)
    release_bundle = create_generic_fk(related_name='releases', to=ReleaseBundle)
    type_product_owner_sign_off = create_generic_enum(choices=SIGN_OFF_CHOICES)

    def __str__(self):
        return f"{self.application.acronym} v{self.version}"

    class Meta:
        ordering = ['-version', '-id']