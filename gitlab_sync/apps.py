from django.apps import AppConfig


class GitlabSyncConfig(AppConfig):
    """
    Django app configuration for GitLab Sync.

    This app provides an improved GitLab synchronization system that runs
    in parallel with the existing git_lab app. It includes:
    - Enhanced error handling and retry logic
    - Support for additional GitLab entities (repositories, commits, pipelines)
    - GitLab Enterprise Edition 17.11.6 specific features (epics, security reports)
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "gitlab_sync"
    verbose_name = "GitLab Sync"
