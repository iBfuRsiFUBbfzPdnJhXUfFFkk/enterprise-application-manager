GITLAB_SYNC_JOB_TYPE_GROUPS: str = "groups"
GITLAB_SYNC_JOB_TYPE_PROJECTS: str = "projects"
GITLAB_SYNC_JOB_TYPE_PIPELINES: str = "pipelines"

# noinspection DuplicatedCode
GITLAB_SYNC_JOB_TYPE_CHOICES: list[tuple[str, str]] = [
    (GITLAB_SYNC_JOB_TYPE_GROUPS, "Groups"),
    (GITLAB_SYNC_JOB_TYPE_PROJECTS, "Projects"),
    (GITLAB_SYNC_JOB_TYPE_PIPELINES, "Pipelines"),
]
