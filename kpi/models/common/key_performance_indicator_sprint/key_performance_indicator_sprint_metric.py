from typing import TypedDict


class KeyPerformanceIndicatorSprintMetric(TypedDict):
    accuracy: float
    capacity: int
    number_of_story_points_committed_to: int
    delivered: int
    reviews: int
    velocity: float