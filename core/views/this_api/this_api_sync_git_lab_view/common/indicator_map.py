from typing import TypedDict


class Indicator(TypedDict):
    number_of_approvals: int
    number_of_code_lines_added: int
    number_of_code_lines_removed: int
    number_of_comments_made: int
    number_of_issues_authored: int
    number_of_issues_committed_to: int
    number_of_issues_delivered_on: int
    number_of_issues_weights_committed_to: int
    number_of_issues_weights_delivered_on: int
    number_of_threads_made: int
    project_ids_worked_on: list[str]


# GitLab id => Indicator
IndicatorMap = dict[str, Indicator]


def create_initial_indicator() -> Indicator:
    return {
        "number_of_approvals": 0,
        "number_of_code_lines_added": 0,
        "number_of_code_lines_removed": 0,
        "number_of_comments_made": 0,
        "number_of_issues_authored": 0,
        "number_of_issues_committed_to": 0,
        "number_of_issues_delivered_on": 0,
        "number_of_issues_weights_committed_to": 0,
        "number_of_issues_weights_delivered_on": 0,
        "number_of_threads_made": 0,
        "project_ids_worked_on": [],
    }


def create_initial_indicator_map() -> IndicatorMap:
    return {}


def ensure_indicator_map(indicator_map: IndicatorMap | None = None) -> IndicatorMap:
    if indicator_map is None:
        return create_initial_indicator_map()
    return indicator_map


def ensure_indicator_is_in_map(
        git_lab_user_id: int | str | None = None,
        indicator_map: IndicatorMap | None = None
) -> IndicatorMap:
    indicator_map: IndicatorMap = ensure_indicator_map(indicator_map=indicator_map)
    if git_lab_user_id is None:
        return indicator_map
    if str(git_lab_user_id) not in indicator_map:
        indicator_map[str(git_lab_user_id)] = create_initial_indicator()
    return indicator_map
