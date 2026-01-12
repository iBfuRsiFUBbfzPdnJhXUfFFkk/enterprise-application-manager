from datetime import datetime

from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.utilities.cast_query_set import cast_query_set
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

    _disable_history = True  # Synced from GitLab - authoritative history exists in external system

    project = models.ForeignKey(
        "gitlab_sync.GitLabSyncProject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="security_reports",
    )
    pipeline = models.ForeignKey(
        "gitlab_sync.GitLabSyncPipeline",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="security_reports",
    )
    report_type: str | None = models.CharField(max_length=255, null=True, blank=True)
    scan_started_at: datetime | None = models.DateTimeField(null=True, blank=True)
    scan_finished_at: datetime | None = models.DateTimeField(null=True, blank=True)
    scanner_name: str | None = models.CharField(max_length=255, null=True, blank=True)
    scanner_vendor: str | None = models.CharField(max_length=255, null=True, blank=True)
    scanner_version: str | None = models.CharField(max_length=255, null=True, blank=True)
    vulnerabilities_count: int | None = models.IntegerField(null=True, blank=True)
    critical_count: int | None = models.IntegerField(null=True, blank=True)
    high_count: int | None = models.IntegerField(null=True, blank=True)
    medium_count: int | None = models.IntegerField(null=True, blank=True)
    low_count: int | None = models.IntegerField(null=True, blank=True)
    info_count: int | None = models.IntegerField(null=True, blank=True)
    unknown_count: int | None = models.IntegerField(null=True, blank=True)

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
