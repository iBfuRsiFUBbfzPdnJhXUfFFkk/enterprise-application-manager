from core.models.application import Application
from core.models.common.comment import Comment
from core.models.common.create_generic_enum import create_generic_enum
from core.models.common.create_generic_fk import create_generic_fk
from core.models.common.create_generic_varchar import create_generic_varchar
from core.models.release_bundle import ReleaseBundle


class Release(Comment):
    SIGN_OFF_APPROVED = "Approved"
    SIGN_OFF_DENIED = "Denied"
    SIGN_OFF_PENDING = "Pending"

    SIGN_OFF_CHOICES = [
        (SIGN_OFF_APPROVED, SIGN_OFF_APPROVED),
        (SIGN_OFF_DENIED, SIGN_OFF_DENIED),
        (SIGN_OFF_PENDING, SIGN_OFF_PENDING),
    ]

    application = create_generic_fk(related_name='releases', to=Application)
    release_bundle = create_generic_fk(related_name='releases', to=ReleaseBundle)
    type_product_owner_sign_off = create_generic_enum(choices=SIGN_OFF_CHOICES)
    version = create_generic_varchar()

    def __str__(self):
        return f"{self.application.acronym} v{self.version}"
