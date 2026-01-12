from django.db import models
from core.models.application import Application
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_version import AbstractVersion
from core.models.common.enums.sign_off_choices import SIGN_OFF_CHOICES
from core.models.release_bundle import ReleaseBundle

class Release(AbstractBaseModel, AbstractComment, AbstractVersion):
    application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True, blank=True, related_name='releases')
    release_bundle = models.ForeignKey(ReleaseBundle, on_delete=models.SET_NULL, null=True, blank=True, related_name='releases')
    type_product_owner_sign_off = models.CharField(max_length=255, choices=SIGN_OFF_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.application.acronym} v{self.version}"

    class Meta:
        ordering = ['-version', '-id']
