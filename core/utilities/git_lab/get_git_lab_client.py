from gitlab import Gitlab

from core.models.secret import Secret
from core.models.this_server_configuration import ThisServerConfiguration


def get_git_lab_client() -> Gitlab | None:
    this_server_configuration: ThisServerConfiguration = ThisServerConfiguration.current()
    connection_git_lab_hostname: str | None = this_server_configuration.connection_git_lab_hostname
    if connection_git_lab_hostname is None:
        return None
    connection_git_lab_api_version: str | None = this_server_configuration.connection_git_lab_api_version
    if connection_git_lab_api_version is None:
        return None
    connection_git_lab_token_secret: Secret | None = this_server_configuration.connection_git_lab_token
    if connection_git_lab_token_secret is None:
        return None
    decrypted_token: str | None = connection_git_lab_token_secret.get_encrypted_value()
    if decrypted_token is None:
        return None
    return Gitlab(
        api_version=connection_git_lab_api_version.replace("v", ""),
        private_token=decrypted_token,
        url=f"https://{connection_git_lab_hostname}/"
    )
