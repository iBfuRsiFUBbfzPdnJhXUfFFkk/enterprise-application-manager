from typing import TypedDict

from kpi.utilities.calculate_sprint_metrics import SprintMetrics


class AverageMetrics(TypedDict):
    accuracy: float
    delivered: float
    reviews: float
    velocity: float


def calculate_average_metrics(
        completed_metrics: list[SprintMetrics | None] | None = None,
) -> AverageMetrics | None:
    if not completed_metrics:
        return None

    total_capacity = sum(m["capacity"] for m in completed_metrics)
    total_delivered = sum(m["delivered"] for m in completed_metrics)
    weighted_velocity = total_delivered / total_capacity if total_capacity else 0
    avg_accuracy = sum(m["accuracy"] for m in completed_metrics) / len(completed_metrics)
    avg_delivered = sum(m["delivered"] for m in completed_metrics) / len(completed_metrics)
    avg_reviews = sum(m["reviews"] for m in completed_metrics) / len(completed_metrics)

    return {
        "accuracy": round(avg_accuracy, 2),
        "delivered": round(avg_delivered, 0),
        "reviews": round(avg_reviews, 0),
        "velocity": round(weighted_velocity, 2),
    }
