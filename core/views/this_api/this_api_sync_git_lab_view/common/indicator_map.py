from typing import TypedDict


class IndicatorMap(TypedDict):
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


def create_initial_indicator_map() -> IndicatorMap:
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
