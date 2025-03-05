from gitlab import Gitlab
from gitlab.v4.objects import Project

from core.utilities.git_lab.get_git_lab_client import get_git_lab_client


def fetch_git_lab_project(
        git_lab_client: Gitlab | None = None,
        project_id: int | str | None = None,
) -> Project | None:
    if git_lab_client is None:
        git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None or project_id is None:
        return None
    return git_lab_client.projects.get(id=project_id, lazy=True)
