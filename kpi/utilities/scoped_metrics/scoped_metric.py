from typing import TypedDict


class ScopedMetric(TypedDict):
    total_accuracy_on_committed_to_story_points: float | None
    total_adjusted_capacity: int | None
    total_merge_requests_approved: int | None
    total_story_points_committed_to: int | None
    total_story_points_delivered: int | None
    total_velocity_of_capacity: float | None


def get_initial_scoped_metric() -> ScopedMetric:
    return {
        "total_accuracy_on_committed_to_story_points": 0.0,
        "total_adjusted_capacity": 0,
        "total_merge_requests_approved": 0,
        "total_story_points_committed_to": 0,
        "total_story_points_delivered": 0,
        "total_velocity_of_capacity": 0.0,
    }
