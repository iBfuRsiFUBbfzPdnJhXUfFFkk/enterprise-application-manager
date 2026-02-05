APPROVAL_STATUS_PENDING: str = "pending"
APPROVAL_STATUS_APPROVED: str = "approved"
APPROVAL_STATUS_REJECTED: str = "rejected"
APPROVAL_STATUS_EXPIRED: str = "expired"

APPROVAL_STATUS_CHOICES: list[tuple[str, str]] = [
    (APPROVAL_STATUS_PENDING, "Pending"),
    (APPROVAL_STATUS_APPROVED, "Approved"),
    (APPROVAL_STATUS_REJECTED, "Rejected"),
    (APPROVAL_STATUS_EXPIRED, "Expired"),
]
