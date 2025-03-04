from core.utilities.git_lab.get_git_lab_url_base_groups import get_git_lab_url_base_groups


def get_git_lab_url_base_groups_members() -> str | None:
    git_lab_url_base_groups: str | None = get_git_lab_url_base_groups()
    if git_lab_url_base_groups is None:
        return None
    return f"{git_lab_url_base_groups}/members/"
