from core.utilities.git_lab.get_git_lab_url_base_projects import get_git_lab_url_base_projects


def get_git_lab_url_base_projects_merge_requests(
        merge_request_internal_identification_iid: int | str | None = None,
        project_id: int | str | None = None,
) -> str | None:
    git_lab_url_base_projects: str | None = get_git_lab_url_base_projects(project_id=project_id)
    if git_lab_url_base_projects is None:
        return None
    if merge_request_internal_identification_iid is None:
        return None
    return (
        f"{git_lab_url_base_projects}"
        f"merge_requests/{str(merge_request_internal_identification_iid)}/"
    )
