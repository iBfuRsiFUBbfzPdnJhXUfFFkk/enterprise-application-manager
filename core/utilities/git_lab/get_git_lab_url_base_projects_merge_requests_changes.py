from core.utilities.git_lab.get_git_lab_url_base_projects_merge_requests import \
    get_git_lab_url_base_projects_merge_requests


def get_git_lab_url_base_projects_merge_requests_changes(
        merge_request_internal_identification_iid: int | str | None = None,
        project_id: int | str | None = None,
) -> str | None:
    git_lab_url_base_projects_merge_requests: str | None = get_git_lab_url_base_projects_merge_requests(
        merge_request_internal_identification_iid=merge_request_internal_identification_iid,
        project_id=project_id
    )
    return f"{git_lab_url_base_projects_merge_requests}/changes/"
