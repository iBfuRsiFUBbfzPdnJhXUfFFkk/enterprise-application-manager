from django.db.models import CharField, ForeignKey, DO_NOTHING

from core.models.application import Application
from core.models.common.comment import Comment
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

    application = ForeignKey(**{
        "blank": True,
        "null": True,
        "on_delete": DO_NOTHING,
        "related_name": 'releases',
        "to": Application,
    })
    release_bundle = ForeignKey(**{
        "blank": True,
        "null": True,
        "on_delete": DO_NOTHING,
        "related_name": 'releases',
        "to": ReleaseBundle,
    })
    version = CharField(blank=True, max_length=255, null=True)
    type_product_owner_sign_off = CharField(blank=True, choices=SIGN_OFF_CHOICES, max_length=255, null=True)

    def __str__(self):
        return f"{self.application.acronym} v{self.version}"
