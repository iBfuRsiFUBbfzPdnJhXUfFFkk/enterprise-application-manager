from gitlab.base import RESTObject

from core.views.this_api.this_api_sync_git_lab_view.common.fetch_issues_by_iteration import \
    fetch_issues_by_iteration


def fetch_issues_by_iterations(
        iteration_ids: list[int | str] | None = None,
) -> list[RESTObject] | None:
    if iteration_ids is None:
        return None
    all_group_issues: list[RESTObject] = []
    for iteration_id in iteration_ids:
        all_group_issues.extend(fetch_issues_by_iteration(iteration_id=iteration_id) or [])
    return all_group_issues
