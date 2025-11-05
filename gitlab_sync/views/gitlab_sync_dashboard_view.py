from django.http import HttpRequest, HttpResponse

from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.base_render import base_render
from gitlab_sync.models import (
    GitLabSyncArtifact,
    GitLabSyncBranch,
    GitLabSyncCommit,
    GitLabSyncEpic,
    GitLabSyncEvent,
    GitLabSyncGroup,
    GitLabSyncIssue,
    GitLabSyncIteration,
    GitLabSyncJob,
    GitLabSyncMergeRequest,
    GitLabSyncMilestone,
    GitLabSyncPipeline,
    GitLabSyncProject,
    GitLabSyncRepository,
    GitLabSyncSecurityReport,
    GitLabSyncSnippet,
    GitLabSyncTag,
    GitLabSyncUser,
    GitLabSyncVulnerability,
)
from gitlab_sync.utilities import cleanup_stale_jobs


def gitlab_sync_dashboard_view(request: HttpRequest) -> HttpResponse:
    """
    GitLab Sync management dashboard view.

    Displays sync statistics, entity counts, and provides sync management controls.
    Automatically cleans up stale jobs on page load.
    """
    # Clean up any stale jobs (running > 60 minutes)
    cleanup_stale_jobs(max_runtime_minutes=60)

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
        "milestones": GitLabSyncMilestone.objects.count(),
        "iterations": GitLabSyncIteration.objects.count(),
        "snippets": GitLabSyncSnippet.objects.count(),
        "events": GitLabSyncEvent.objects.count(),
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

    config = ThisServerConfiguration.current()
    gitlab_configured = bool(
        config.connection_git_lab_hostname
        and config.connection_git_lab_token
        and config.connection_git_lab_top_level_group_id
    )

    sync_limits = {
        "max_group_depth": config.coerced_gitlab_sync_max_group_depth,
        "max_projects_per_group": config.coerced_gitlab_sync_max_projects_per_group,
        "pipelines_days_back": config.coerced_gitlab_sync_pipelines_days_back,
        "max_pipelines_per_project": config.coerced_gitlab_sync_max_pipelines_per_project,
        "commits_days_back": config.coerced_gitlab_sync_commits_days_back,
        "max_issues_per_project": config.coerced_gitlab_sync_max_issues_per_project,
        "max_merge_requests_per_project": config.coerced_gitlab_sync_max_merge_requests_per_project,
        "max_events_per_project": config.coerced_gitlab_sync_max_events_per_project,
    }

    context = {
        "stats": stats,
        "recent_projects": recent_projects,
        "recent_pipelines": recent_pipelines,
        "recent_merge_requests": recent_merge_requests,
        "pipeline_stats": pipeline_stats,
        "mr_stats": mr_stats,
        "vulnerability_stats": vulnerability_stats,
        "gitlab_configured": gitlab_configured,
        "gitlab_hostname": config.connection_git_lab_hostname,
        "gitlab_group_id": config.connection_git_lab_top_level_group_id,
        "sync_limits": sync_limits,
    }

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/dashboard.html",
        context=context,
    )
