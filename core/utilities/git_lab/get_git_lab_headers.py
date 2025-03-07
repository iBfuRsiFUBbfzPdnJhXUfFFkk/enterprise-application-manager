from typing import Mapping, Literal

from core.models.secret import Secret
from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.this_server_configuration.get_current_server_configuration import get_current_server_configuration

GitLabHeaders = Mapping[Literal["PRIVATE-TOKEN"], str]


def get_git_lab_headers() -> GitLabHeaders | None:
    this_server_configuration: ThisServerConfiguration | None = get_current_server_configuration()
    if this_server_configuration is None:
        return None
    connection_git_lab_token_secret: Secret | None = this_server_configuration.connection_git_lab_token
    if connection_git_lab_token_secret is None:
        return None
    decrypted_token: str | None = connection_git_lab_token_secret.get_encrypted_value()
    if decrypted_token is None:
        return None
    return {
        "PRIVATE-TOKEN": decrypted_token
    }
