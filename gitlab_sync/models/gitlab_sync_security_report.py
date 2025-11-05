from datetime import datetime

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.utilities.cast_query_set import cast_query_set
from django_generic_model_fields.create_generic_datetime import create_generic_datetime
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_integer import create_generic_integer
from django_generic_model_fields.create_generic_varchar import create_generic_varchar
from gitlab_sync.models.common.abstract import (
    AbstractGitLabCreatedAt,
    AbstractGitLabPrimaryKey,
)


class GitLabSyncSecurityReport(
    AbstractBaseModel,
    AbstractGitLabCreatedAt,
    AbstractGitLabPrimaryKey,
):
    """
    Represents a security scanning report from GitLab EE 17.11.6.

    GitLab EE provides multiple security scanning types:
    - SAST (Static Application Security Testing)
    - DAST (Dynamic Application Security Testing)
    - Dependency Scanning
    - Container Scanning
    - Secret Detection
    - Coverage Fuzzing
    """

    project = create_generic_fk(
        related_name="security_reports",
        to="gitlab_sync.GitLabSyncProject",
    )
    pipeline = create_generic_fk(
        related_name="security_reports",
        to="gitlab_sync.GitLabSyncPipeline",
    )
    report_type: str | None = create_generic_varchar()
    scan_started_at: datetime | None = create_generic_datetime()
    scan_finished_at: datetime | None = create_generic_datetime()
    scanner_name: str | None = create_generic_varchar()
    scanner_vendor: str | None = create_generic_varchar()
    scanner_version: str | None = create_generic_varchar()
    vulnerabilities_count: int | None = create_generic_integer()
    critical_count: int | None = create_generic_integer()
    high_count: int | None = create_generic_integer()
    medium_count: int | None = create_generic_integer()
    low_count: int | None = create_generic_integer()
    info_count: int | None = create_generic_integer()
    unknown_count: int | None = create_generic_integer()

    @property
    def vulnerabilities(self):
        from gitlab_sync.models.gitlab_sync_vulnerability import GitLabSyncVulnerability

        return cast_query_set(
            typ=GitLabSyncVulnerability,
            val=GitLabSyncVulnerability.objects.filter(report=self),
        )

    def __str__(self) -> str:
        return f"{self.report_type} Report #{self.id}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "GitLab Sync Security Report"
        verbose_name_plural = "GitLab Sync Security Reports"
