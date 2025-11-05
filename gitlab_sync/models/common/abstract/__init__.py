# Import existing abstract models from git_lab app for consistency
from git_lab.models.common.abstract.abstract_git_lab_avatar_url import (
    AbstractGitLabAvatarUrl,
)
from git_lab.models.common.abstract.abstract_git_lab_closed_at import (
    AbstractGitLabClosedAt,
)
from git_lab.models.common.abstract.abstract_git_lab_created_at import (
    AbstractGitLabCreatedAt,
)
from git_lab.models.common.abstract.abstract_git_lab_description import (
    AbstractGitLabDescription,
)
from git_lab.models.common.abstract.abstract_git_lab_internal_identification import (
    AbstractGitLabInternalIdentification,
)
from git_lab.models.common.abstract.abstract_git_lab_path import AbstractGitLabPath
from git_lab.models.common.abstract.abstract_git_lab_primary_key import (
    AbstractGitLabPrimaryKey,
)
from git_lab.models.common.abstract.abstract_git_lab_references import (
    AbstractGitLabReferences,
)
from git_lab.models.common.abstract.abstract_git_lab_state import AbstractGitLabState
from git_lab.models.common.abstract.abstract_git_lab_task_completion_status import (
    AbstractGitLabTaskCompletionStatus,
)
from git_lab.models.common.abstract.abstract_git_lab_time_stats import (
    AbstractGitLabTimeStats,
)
from git_lab.models.common.abstract.abstract_git_lab_title import AbstractGitLabTitle
from git_lab.models.common.abstract.abstract_git_lab_updated_at import (
    AbstractGitLabUpdatedAt,
)
from git_lab.models.common.abstract.abstract_git_lab_web_url import (
    AbstractGitLabWebUrl,
)

__all__ = [
    "AbstractGitLabAvatarUrl",
    "AbstractGitLabClosedAt",
    "AbstractGitLabCreatedAt",
    "AbstractGitLabDescription",
    "AbstractGitLabInternalIdentification",
    "AbstractGitLabPath",
    "AbstractGitLabPrimaryKey",
    "AbstractGitLabReferences",
    "AbstractGitLabState",
    "AbstractGitLabTaskCompletionStatus",
    "AbstractGitLabTimeStats",
    "AbstractGitLabTitle",
    "AbstractGitLabUpdatedAt",
    "AbstractGitLabWebUrl",
]
