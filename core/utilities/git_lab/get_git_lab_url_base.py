from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.this_server_configuration.get_current_server_configuration import get_current_server_configuration


def get_git_lab_url_base() -> str | None:
    this_server_configuration: ThisServerConfiguration | None = get_current_server_configuration()
    if this_server_configuration is None:
        return None
    connection_git_lab_hostname: str | None = this_server_configuration.connection_git_lab_hostname
    if connection_git_lab_hostname is None:
        return None
    connection_git_lab_api_version: str | None = this_server_configuration.connection_git_lab_api_version
    if connection_git_lab_api_version is None:
        return None
    return (
        f"https://{connection_git_lab_hostname}/"
        f"api/v{connection_git_lab_api_version}/"
    )
