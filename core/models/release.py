from core.models.application import Application
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_version import AbstractVersion
from core.models.common.enums.sign_off_choices import SIGN_OFF_CHOICES
from django_generic_model_fields.create_generic_enum import create_generic_enum
from django_generic_model_fields.create_generic_fk import create_generic_fk
from core.models.release_bundle import ReleaseBundle


class Release(AbstractBaseModel, AbstractComment, AbstractVersion):
    application = create_generic_fk(related_name='releases', to=Application)
    release_bundle = create_generic_fk(related_name='releases', to=ReleaseBundle)
    type_product_owner_sign_off = create_generic_enum(choices=SIGN_OFF_CHOICES)

    def __str__(self):
        return f"{self.application.acronym} v{self.version}"

    class Meta:
        ordering = ['-version', '-id']
