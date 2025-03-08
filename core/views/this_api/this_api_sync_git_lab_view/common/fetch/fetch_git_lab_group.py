from gitlab import Gitlab
from gitlab.v4.objects import Group

from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client


def fetch_git_lab_group(
        git_lab_client: Gitlab | None = None,
) -> Group | None:
    if git_lab_client is None:
        git_lab_client: Gitlab | None = get_git_lab_client()
    connection_git_lab_top_level_group_id: str | None = ThisServerConfiguration.current().connection_git_lab_top_level_group_id
    if git_lab_client is None or connection_git_lab_top_level_group_id is None:
        return None
    return git_lab_client.groups.get(id=connection_git_lab_top_level_group_id, lazy=True)
