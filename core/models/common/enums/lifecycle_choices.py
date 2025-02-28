LIFECYCLE_ACTIVE: str = "Active"
LIFECYCLE_APPROVAL: str = "Awaiting Approval"
LIFECYCLE_DEPRECATED: str = "Deprecated"
LIFECYCLE_DEVELOPMENT: str = "In Development"
LIFECYCLE_HYPER_CARE: str = "Hyper Care"
LIFECYCLE_IDEA: str = "Idea Submission"
LIFECYCLE_IN_DEPRECATION: str = "In Deprecation Period"
LIFECYCLE_LIMITED_SUPPORT: str = "Limited Support"
LIFECYCLE_PLANNING: str = "In Planning"
LIFECYCLE_REJECTED: str = "Approval Rejected"

# noinspection DuplicatedCode
LIFECYCLE_CHOICES: list[tuple[str, str]] = [
    (LIFECYCLE_ACTIVE, LIFECYCLE_ACTIVE),
    (LIFECYCLE_APPROVAL, LIFECYCLE_APPROVAL),
    (LIFECYCLE_DEPRECATED, LIFECYCLE_DEPRECATED),
    (LIFECYCLE_DEVELOPMENT, LIFECYCLE_DEVELOPMENT),
    (LIFECYCLE_HYPER_CARE, LIFECYCLE_HYPER_CARE),
    (LIFECYCLE_IDEA, LIFECYCLE_IDEA),
    (LIFECYCLE_IN_DEPRECATION, LIFECYCLE_IN_DEPRECATION),
    (LIFECYCLE_LIMITED_SUPPORT, LIFECYCLE_LIMITED_SUPPORT),
    (LIFECYCLE_PLANNING, LIFECYCLE_PLANNING),
    (LIFECYCLE_REJECTED, LIFECYCLE_REJECTED),
]
