from typing import TypedDict


class ChartDataModel(TypedDict):
    accuracy: list[float] | None
    labels: list[str] | None
    velocity: list[float] | None
