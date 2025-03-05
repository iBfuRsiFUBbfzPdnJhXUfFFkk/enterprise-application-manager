from gitlab import Gitlab
from gitlab.v4.objects import Group

from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.utilities.git_lab.get_git_lab_group_id import get_git_lab_group_id


def fetch_git_lab_group(
        git_lab_client: Gitlab | None = None,
) -> Group | None:
    if git_lab_client is None:
        git_lab_client: Gitlab | None = get_git_lab_client()
    git_lab_group_id: str | None = get_git_lab_group_id()
    if git_lab_client is None or git_lab_group_id is None:
        return None
    return git_lab_client.groups.get(id=git_lab_group_id, lazy=True)
