from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render
from gitlab_sync.models import (
    GitLabSyncArtifact,
    GitLabSyncBranch,
    GitLabSyncCommit,
    GitLabSyncEpic,
    GitLabSyncGroup,
    GitLabSyncIssue,
    GitLabSyncJob,
    GitLabSyncMergeRequest,
    GitLabSyncPipeline,
    GitLabSyncProject,
    GitLabSyncRepository,
    GitLabSyncSecurityReport,
    GitLabSyncTag,
    GitLabSyncUser,
    GitLabSyncVulnerability,
)


def gitlab_sync_dashboard_view(request: HttpRequest) -> HttpResponse:
    """
    GitLab Sync management dashboard view.

    Displays sync statistics, entity counts, and provides sync management controls.
    """
    stats = {
        "groups": GitLabSyncGroup.objects.count(),
        "projects": GitLabSyncProject.objects.count(),
        "users": GitLabSyncUser.objects.count(),
        "issues": GitLabSyncIssue.objects.count(),
        "merge_requests": GitLabSyncMergeRequest.objects.count(),
        "repositories": GitLabSyncRepository.objects.count(),
        "commits": GitLabSyncCommit.objects.count(),
        "branches": GitLabSyncBranch.objects.count(),
        "tags": GitLabSyncTag.objects.count(),
        "pipelines": GitLabSyncPipeline.objects.count(),
        "jobs": GitLabSyncJob.objects.count(),
        "artifacts": GitLabSyncArtifact.objects.count(),
        "epics": GitLabSyncEpic.objects.count(),
        "security_reports": GitLabSyncSecurityReport.objects.count(),
        "vulnerabilities": GitLabSyncVulnerability.objects.count(),
    }

    stats["total_entities"] = sum(stats.values())

    recent_projects = GitLabSyncProject.objects.order_by("-updated_at")[:5]
    recent_pipelines = GitLabSyncPipeline.objects.order_by("-created_at")[:5]
    recent_merge_requests = GitLabSyncMergeRequest.objects.order_by("-updated_at")[:5]

    pipeline_stats = {
        "total": GitLabSyncPipeline.objects.count(),
        "success": GitLabSyncPipeline.objects.filter(status="success").count(),
        "failed": GitLabSyncPipeline.objects.filter(status="failed").count(),
        "running": GitLabSyncPipeline.objects.filter(status="running").count(),
        "pending": GitLabSyncPipeline.objects.filter(status="pending").count(),
    }

    mr_stats = {
        "total": GitLabSyncMergeRequest.objects.count(),
        "merged": GitLabSyncMergeRequest.objects.filter(state="merged").count(),
        "opened": GitLabSyncMergeRequest.objects.filter(state="opened").count(),
        "closed": GitLabSyncMergeRequest.objects.filter(state="closed").count(),
    }

    vulnerability_stats = {
        "total": GitLabSyncVulnerability.objects.count(),
        "critical": GitLabSyncVulnerability.objects.filter(severity="critical").count(),
        "high": GitLabSyncVulnerability.objects.filter(severity="high").count(),
        "medium": GitLabSyncVulnerability.objects.filter(severity="medium").count(),
        "low": GitLabSyncVulnerability.objects.filter(severity="low").count(),
    }

    context = {
        "stats": stats,
        "recent_projects": recent_projects,
        "recent_pipelines": recent_pipelines,
        "recent_merge_requests": recent_merge_requests,
        "pipeline_stats": pipeline_stats,
        "mr_stats": mr_stats,
        "vulnerability_stats": vulnerability_stats,
    }

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/dashboard.html",
        context=context,
    )
