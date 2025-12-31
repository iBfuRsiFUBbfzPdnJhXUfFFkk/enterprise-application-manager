TASK_STATUS_TO_DO: str = "to_do"
TASK_STATUS_IN_PROGRESS: str = "in_progress"
TASK_STATUS_IN_REVIEW: str = "in_review"
TASK_STATUS_COMPLETED: str = "completed"
TASK_STATUS_CANCELLED: str = "cancelled"

TASK_STATUS_CHOICES: list[tuple[str, str]] = [
    (TASK_STATUS_TO_DO, "To Do"),
    (TASK_STATUS_IN_PROGRESS, "In Progress"),
    (TASK_STATUS_IN_REVIEW, "In Review"),
    (TASK_STATUS_COMPLETED, "Completed"),
    (TASK_STATUS_CANCELLED, "Cancelled"),
]
