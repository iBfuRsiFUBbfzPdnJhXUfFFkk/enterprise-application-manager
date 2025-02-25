from core.models.application import Application
from core.models.common.abstract.comment import Comment
from core.models.common.abstract.version import Version
from core.models.common.enums.data_storage_form_choices import DATA_STORAGE_FORM_CHOICES
from core.models.common.enums.database_flavor_choices import DATABASE_FLAVOR_CHOICES
from core.models.common.enums.environment_choices import ENVIRONMENT_CHOICES
from core.models.common.field_factories.create_generic_enum import create_generic_enum
from core.models.common.field_factories.create_generic_fk import create_generic_fk


class Database(Comment, Version):
    application = create_generic_fk(related_name='databases', to=Application)
    type_data_storage_form = create_generic_enum(choices=DATA_STORAGE_FORM_CHOICES)
    type_database_flavor = create_generic_enum(choices=DATABASE_FLAVOR_CHOICES)
    type_environment = create_generic_enum(choices=ENVIRONMENT_CHOICES)

    def __str__(self):
        return f"{self.application.acronym} - {self.type_environment} - v{self.version}"
