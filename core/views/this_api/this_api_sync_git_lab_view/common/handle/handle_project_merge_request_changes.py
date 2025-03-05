from gitlab import Gitlab
from gitlab.v4.objects import Project, ProjectMergeRequest

from core.views.this_api.this_api_sync_git_lab_view.common.fetch.fetch_project_merge_requests_changes import \
    fetch_project_merge_requests_changes
from core.views.this_api.this_api_sync_git_lab_view.common.indicator_map import ensure_indicator_map, \
    IndicatorMap
from core.views.this_api.this_api_sync_git_lab_view.common.models.git_lab_api_change import GitLabApiChange


def handle_project_merge_request_changes(
        git_lab_client: Gitlab | None = None,
        git_lab_project: Project | None = None,
        indicator_map: IndicatorMap | None = None,
        merge_request_author_id: str | None = None,
        merge_request_internal_identification_iid: int | None = None,
        project_id: int | None = None,
        project_merge_request: ProjectMergeRequest | None = None,
) -> IndicatorMap:
    indicator_map: IndicatorMap = ensure_indicator_map(indicator_map=indicator_map)
    changes: list[GitLabApiChange] | None = fetch_project_merge_requests_changes(
        git_lab_client=git_lab_client,
        git_lab_project=git_lab_project,
        merge_request_internal_identification_iid=merge_request_internal_identification_iid,
        project_id=project_id,
        project_merge_request=project_merge_request
    )
    if changes is None:
        return indicator_map
    for change in changes:
        diff_text: str | None = change["diff"]
        if diff_text is None:
            continue
        for line in diff_text.splitlines():
            if line.startswith('+'):
                indicator_map[merge_request_author_id]["number_of_code_lines_added"] += 1
            elif line.startswith('-'):
                indicator_map[merge_request_author_id]["number_of_code_lines_removed"] += 1
    return indicator_map
