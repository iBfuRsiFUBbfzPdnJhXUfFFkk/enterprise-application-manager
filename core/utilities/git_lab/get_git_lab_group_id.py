from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.this_server_configuration.get_current_server_configuration import get_current_server_configuration


def get_git_lab_group_id() -> str | None:
    this_server_configuration: ThisServerConfiguration | None = get_current_server_configuration()
    if this_server_configuration is None:
        return None
    return this_server_configuration.connection_git_lab_group_id
