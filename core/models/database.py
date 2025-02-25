from core.models.application import Application
from core.models.common.comment import Comment
from core.models.common.create_generic_enum import create_generic_enum
from core.models.common.create_generic_fk import create_generic_fk
from core.models.common.create_generic_varchar import create_generic_varchar


class Database(Comment):
    DATABASE_TYPE_BLOB = "Blob"
    DATABASE_TYPE_DOCUMENT = "Document"
    DATABASE_TYPE_RELATIONAL = "Relational"

    DATABASE_FLAVOR_MARIADB = "MariaDB"
    DATABASE_FLAVOR_POSTGRESQL = "PostgreSQL"

    DATABASE_ENVIRONMENT_LOCAL = "Local"
    DATABASE_ENVIRONMENT_DEVELOPMENT = "Development"
    DATABASE_ENVIRONMENT_STAGING = "Staging"
    DATABASE_ENVIRONMENT_PRODUCTION = "Production"

    DATABASE_ENVIRONMENT_CHOICES = [
        (DATABASE_ENVIRONMENT_LOCAL, DATABASE_ENVIRONMENT_LOCAL),
        (DATABASE_ENVIRONMENT_DEVELOPMENT, DATABASE_ENVIRONMENT_DEVELOPMENT),
        (DATABASE_ENVIRONMENT_STAGING, DATABASE_ENVIRONMENT_STAGING),
        (DATABASE_ENVIRONMENT_PRODUCTION, DATABASE_ENVIRONMENT_PRODUCTION),
    ]

    DATABASE_FLAVOR_CHOICES = [
        (DATABASE_FLAVOR_MARIADB, DATABASE_FLAVOR_MARIADB),
        (DATABASE_FLAVOR_POSTGRESQL, DATABASE_FLAVOR_POSTGRESQL),
    ]

    DATABASE_TYPE_CHOICES = [
        (DATABASE_TYPE_BLOB, DATABASE_TYPE_BLOB),
        (DATABASE_TYPE_DOCUMENT, DATABASE_TYPE_DOCUMENT),
        (DATABASE_TYPE_RELATIONAL, DATABASE_TYPE_RELATIONAL),
    ]

    application = create_generic_fk(related_name='databases', to=Application)
    database_name = create_generic_varchar()
    type_database_environment = create_generic_enum(choices=DATABASE_ENVIRONMENT_CHOICES)
    type_database_flavor = create_generic_enum(choices=DATABASE_FLAVOR_CHOICES)
    type_database_storage_model = create_generic_enum(choices=DATABASE_TYPE_CHOICES)
    version = create_generic_varchar()

    def __str__(self):
        return f"{self.application.acronym} - {self.type_database_environment} - v{self.version}"
