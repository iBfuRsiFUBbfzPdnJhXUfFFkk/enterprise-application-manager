from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.git_lab.get_git_lab_url_base import get_git_lab_url_base
from core.utilities.this_server_configuration.get_current_server_configuration import get_current_server_configuration


def get_git_lab_url_base_groups() -> str | None:
    this_server_configuration: ThisServerConfiguration | None = get_current_server_configuration()
    if this_server_configuration is None:
        return None
    connection_git_lab_group_id: str | None = this_server_configuration.connection_git_lab_group_id
    if connection_git_lab_group_id is None:
        return None
    git_lab_url_base: str | None = get_git_lab_url_base()
    if git_lab_url_base is None:
        return None
    return (
        f"{git_lab_url_base}"
        f"groups/{str(connection_git_lab_group_id)}/"
    )
