from gitlab import Gitlab

from core.models.secret import Secret
from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.this_server_configuration.get_current_server_configuration import get_current_server_configuration


def get_git_lab_client() -> Gitlab | None:
    this_server_configuration: ThisServerConfiguration | None = get_current_server_configuration()
    if this_server_configuration is None:
        return None
    connection_gitlab_hostname: str | None = this_server_configuration.connection_gitlab_hostname
    if connection_gitlab_hostname is None:
        return None
    connection_gitlab_api_version: str | None = this_server_configuration.connection_gitlab_api_version
    if connection_gitlab_api_version is None:
        return None
    connection_gitlab_token_secret: Secret | None = this_server_configuration.connection_gitlab_token
    if connection_gitlab_token_secret is None:
        return None
    decrypted_token: str | None = connection_gitlab_token_secret.get_encrypted_value()
    if decrypted_token is None:
        return None
    return Gitlab(
        api_version=connection_gitlab_api_version.replace("v", ""),
        private_token=decrypted_token,
        url=connection_gitlab_hostname
    )
