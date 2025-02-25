from django.db.models import CharField, ForeignKey, DO_NOTHING

from core.models.application import Application
from core.models.common.comment import Comment


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

    application = ForeignKey(**{
        "blank": True,
        "null": True,
        "on_delete": DO_NOTHING,
        "related_name": 'databases',
        "to": Application,
    })
    database_name = CharField(blank=True, max_length=255, null=True)
    version = CharField(blank=True, max_length=255, null=True)
    type_database_environment = CharField(blank=True, choices=DATABASE_ENVIRONMENT_CHOICES, max_length=255, null=True)
    type_database_flavor = CharField(blank=True, choices=DATABASE_FLAVOR_CHOICES, max_length=255, null=True)
    type_database_storage_model = CharField(blank=True, choices=DATABASE_TYPE_CHOICES, max_length=255, null=True)

    def __str__(self):
        return f"{self.application.acronym} - {self.type_database_environment} - v{self.version}"
