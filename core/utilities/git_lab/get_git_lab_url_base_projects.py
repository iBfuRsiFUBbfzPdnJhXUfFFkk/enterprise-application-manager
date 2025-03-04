from core.utilities.git_lab.get_git_lab_url_base import get_git_lab_url_base


def get_git_lab_url_base_projects(
        project_id: int | str | None = None,
) -> str | None:
    git_lab_url_base: str | None = get_git_lab_url_base()
    if git_lab_url_base is None:
        return None
    if project_id is None:
        return None
    return (
        f"{git_lab_url_base}"
        f"projects/{str(project_id)}/"
    )
