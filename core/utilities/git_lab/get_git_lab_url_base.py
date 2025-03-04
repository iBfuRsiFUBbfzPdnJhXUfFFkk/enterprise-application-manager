from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.this_server_configuration.get_current_server_configuration import get_current_server_configuration


def get_git_lab_url_base() -> str | None:
    this_server_configuration: ThisServerConfiguration | None = get_current_server_configuration()
    if this_server_configuration is None:
        return None
    connection_gitlab_hostname: str | None = this_server_configuration.connection_gitlab_hostname
    if connection_gitlab_hostname is None:
        return None
    connection_gitlab_api_version: str | None = this_server_configuration.connection_gitlab_api_version
    if connection_gitlab_api_version is None:
        return None
    return (
        f"https://{connection_gitlab_hostname}/"
        f"api/{connection_gitlab_api_version}/"
    )
