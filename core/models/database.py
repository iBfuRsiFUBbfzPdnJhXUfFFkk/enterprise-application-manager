from django.db import models
from core.models.application import Application
from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_version import AbstractVersion
from core.models.common.enums.data_storage_form_choices import DATA_STORAGE_FORM_CHOICES
from core.models.common.enums.database_authentication_method_choices import DATABASE_AUTH_METHOD_CHOICES
from core.models.common.enums.database_connection_type_choices import DATABASE_CONNECTION_TYPE_CHOICES
from core.models.common.enums.database_flavor_choices import DATABASE_FLAVOR_CHOICES
from core.models.common.enums.environment_choices import ENVIRONMENT_CHOICES
from core.models.common.enums.ssl_support_choices import SSL_SUPPORT_CHOICES
from core.utilities.encryption import encrypt_secret, decrypt_secret


class Database(AbstractBaseModel, AbstractComment, AbstractVersion):
    application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True, blank=True, related_name='databases')
    encrypted_password = models.CharField(max_length=255, null=True, blank=True)
    encrypted_username = models.CharField(max_length=255, null=True, blank=True)
    hostname = models.CharField(max_length=255, null=True, blank=True)
    ip_v4_internal = models.CharField(max_length=255, null=True, blank=True)
    port = models.IntegerField(null=True, blank=True)
    schema = models.CharField(max_length=255, null=True, blank=True)
    type_data_storage_form = models.CharField(max_length=255, choices=DATA_STORAGE_FORM_CHOICES, null=True, blank=True)
    type_database_flavor = models.CharField(max_length=255, choices=DATABASE_FLAVOR_CHOICES, null=True, blank=True)
    type_environment = models.CharField(max_length=255, choices=ENVIRONMENT_CHOICES, null=True, blank=True)

    # Network and Security Fields
    is_public_facing = models.BooleanField(null=True, blank=True, default=False, help_text='Is this database accessible from the public internet?')
    is_read_only = models.BooleanField(null=True, blank=True, default=False, help_text='Is this database connection read-only?')
    type_authentication_method = models.CharField(max_length=255, choices=DATABASE_AUTH_METHOD_CHOICES, null=True, blank=True)
    type_connection_type = models.CharField(max_length=255, choices=DATABASE_CONNECTION_TYPE_CHOICES, null=True, blank=True)
    type_ssl_support = models.CharField(max_length=255, choices=SSL_SUPPORT_CHOICES, null=True, blank=True)

    # SSH Tunnel Configuration
    is_ssh_tunnel_required = models.BooleanField(null=True, blank=True, default=False, help_text='Does this database require SSH tunneling?')
    ssh_tunnel_host = models.CharField(max_length=255, null=True, blank=True, help_text='SSH tunnel hostname')
    ssh_tunnel_port = models.IntegerField(null=True, blank=True, help_text='SSH tunnel port (usually 22)')
    encrypted_ssh_tunnel_username = models.CharField(max_length=255, null=True, blank=True)
    encrypted_ssh_tunnel_password = models.CharField(max_length=255, null=True, blank=True)

    # Certificate Management
    is_certificate_required = models.BooleanField(null=True, blank=True, default=False, help_text='Does this connection require an SSL/TLS certificate?')
    certificate = models.ForeignKey('Document', on_delete=models.SET_NULL, null=True, blank=True, related_name='databases_using_certificate', help_text='SSL/TLS certificate file')

    def set_encrypted_password(self, secret: str | None) -> None:
        self.encrypted_password = encrypt_secret(secret=secret)

    def get_encrypted_password(self) -> str | None:
        return decrypt_secret(encrypted_secret=self.encrypted_password)

    def set_encrypted_username(self, secret: str | None) -> None:
        self.encrypted_username = encrypt_secret(secret=secret)

    def get_encrypted_username(self) -> str | None:
        return decrypt_secret(encrypted_secret=self.encrypted_username)

    def set_encrypted_ssh_tunnel_username(self, secret: str | None) -> None:
        self.encrypted_ssh_tunnel_username = encrypt_secret(secret=secret)

    def get_encrypted_ssh_tunnel_username(self) -> str | None:
        return decrypt_secret(encrypted_secret=self.encrypted_ssh_tunnel_username)

    def set_encrypted_ssh_tunnel_password(self, secret: str | None) -> None:
        self.encrypted_ssh_tunnel_password = encrypt_secret(secret=secret)

    def get_encrypted_ssh_tunnel_password(self) -> str | None:
        return decrypt_secret(encrypted_secret=self.encrypted_ssh_tunnel_password)

    def get_connection_string(self) -> str | None:
        """Generate a connection string based on database flavor"""
        username = self.get_encrypted_username()
        password = self.get_encrypted_password()
        hostname = self.hostname
        port = self.port
        schema = self.schema
        flavor = self.type_database_flavor

        # Return None if essential fields are missing
        if not hostname or not flavor:
            return None

        # PostgreSQL
        if flavor == "PostgreSQL":
            if username and password and port and schema:
                return f"postgresql://{username}:{password}@{hostname}:{port}/{schema}"
            elif username and password and schema:
                return f"postgresql://{username}:{password}@{hostname}/{schema}"
            return None

        # MariaDB
        elif flavor == "MariaDB":
            if username and password and port and schema:
                return f"mysql://{username}:{password}@{hostname}:{port}/{schema}"
            elif username and password and schema:
                return f"mysql://{username}:{password}@{hostname}/{schema}"
            return None

        # MongoDB
        elif flavor == "MongoDB":
            if username and password and port and schema:
                return f"mongodb://{username}:{password}@{hostname}:{port}/{schema}"
            elif username and password and port:
                return f"mongodb://{username}:{password}@{hostname}:{port}"
            elif port:
                return f"mongodb://{hostname}:{port}"
            return f"mongodb://{hostname}"

        # SQLite
        elif flavor == "SQLite":
            if schema:
                return f"sqlite:///{schema}"
            return None

        # CosmosDB
        elif flavor == "CosmosDB":
            if password:  # Password serves as AccountKey
                return f"AccountEndpoint=https://{hostname}/;AccountKey={password};"
            return None

        # MinIO
        elif flavor == "MinIO":
            if username and password and port and schema:
                return f"s3://{username}:{password}@{hostname}:{port}/{schema}"
            elif username and password and schema:
                return f"s3://{username}:{password}@{hostname}/{schema}"
            return None

        # Azure Blob Storage
        elif flavor == "Azure Blob Storage":
            if username and password:  # username is account name, password is account key
                return f"DefaultEndpointsProtocol=https;AccountName={username};AccountKey={password};EndpointSuffix=core.windows.net"
            return None

        # Unknown flavor
        return None

    def __str__(self):
        return f"{self.application.acronym if self.application is not None else 'N/A'} - {self.type_environment} - v{self.version}"

    class Meta:
        ordering = ['schema', '-id']
