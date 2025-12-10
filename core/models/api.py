from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_m2m import create_generic_m2m
from django_generic_model_fields.create_generic_varchar import create_generic_varchar


class API(AbstractBaseModel, AbstractComment, AbstractName):
    url_local = create_generic_varchar()
    url_development = create_generic_varchar()
    url_staging = create_generic_varchar()
    url_production = create_generic_varchar()
    url_production_external = create_generic_varchar()
    url_documentation = create_generic_varchar()

    service_provider = create_generic_fk(
        to='ServiceProvider',
        related_name='apis'
    )
    tool = create_generic_fk(to='Tool', related_name='apis')
    dependencies = create_generic_m2m(to='Dependency', related_name='apis')
    applications = create_generic_m2m(to='Application', related_name='apis')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "API"
        verbose_name_plural = "APIs"
        ordering = ['name', '-id']
