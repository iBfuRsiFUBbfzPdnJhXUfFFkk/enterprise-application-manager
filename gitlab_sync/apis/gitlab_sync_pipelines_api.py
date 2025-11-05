from datetime import datetime, timedelta
from typing import cast

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from gitlab import Gitlab
from gitlab.v4.objects import Project, ProjectPipeline

from core.models.this_server_configuration import ThisServerConfiguration
from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import (
    convert_and_enforce_utc_timezone,
)
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from core.views.generic.generic_500 import generic_500
from git_lab.apis.common.get_common_query_parameters import (
    GitLabApiCommonQueryParameters,
    get_common_query_parameters,
)
from gitlab_sync.models import (
    GitLabSyncJobTracker,
    GitLabSyncPipeline,
    GitLabSyncProject,
    GitLabSyncUser,
)
from gitlab_sync.utilities import (
    SyncResult,
    check_job_cancelled,
    handle_gitlab_api_errors,
    run_sync_in_background,
)


def _sync_pipelines_background(
    request: HttpRequest, job_tracker: GitLabSyncJobTracker
) -> None:
    """Background function to sync pipelines with progress tracking."""
    sync_result = SyncResult(
        entity_type="GitLabSyncPipeline", job_tracker_id=job_tracker.id
    )
    sync_result.add_log("Starting pipelines sync...")

    query_parameters: GitLabApiCommonQueryParameters = get_common_query_parameters(
        request=request
    )

    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        sync_result.add_log("❌ Failed to get GitLab client")
        sync_result.add_failure("Failed to get GitLab client")
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return

    config = ThisServerConfiguration.current()
    max_pipelines_per_project = config.coerced_gitlab_sync_max_pipelines_per_project
    days_back = config.coerced_gitlab_sync_pipelines_days_back

    # Calculate date cutoff for filtering pipelines
    cutoff_date = datetime.now() - timedelta(days=days_back)
    updated_after = cutoff_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    projects: QuerySet[GitLabSyncProject] = cast_query_set(
        typ=GitLabSyncProject,
        val=GitLabSyncProject.objects.all(),
    )

    project_count = projects.count()
    sync_result.add_log(
        f"Syncing pipelines from {project_count} projects incrementally "
        f"(max {max_pipelines_per_project} per project, last {days_back} days)..."
    )

    # Update query params to limit pipelines per project and filter by date
    limited_query_parameters = {
        **query_parameters,
        "per_page": max_pipelines_per_project,
        "updated_after": updated_after,
    }

    processed_count = 0
    estimated_total = project_count * 5  # Rough estimate

    for proj_idx, project in enumerate(projects, 1):
        # Check if job was cancelled
        if check_job_cancelled(sync_result.job_tracker_id):
            sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
            sync_result.finish()
            print(f"[GitLabSync] {sync_result}")
            return

        pipelines, error = handle_gitlab_api_errors(
            func=lambda: [
                p.asdict()
                for p in cast(
                    list[ProjectPipeline],
                    git_lab_client.projects.get(id=project.id, lazy=True)
                    .pipelines.list(**limited_query_parameters),
                )
            ],
            entity_name=f"Pipelines for project {project.path_with_namespace}",
            max_retries=3,
        )

        if error:
            sync_result.add_log(
                f"❌ Error fetching pipelines for {project.path_with_namespace}: {error}"
            )
            sync_result.add_failure(error)
            continue

        if not pipelines:
            continue

        # Process each pipeline immediately
        for pipeline_dict in pipelines:
            # Check if job was cancelled
            if check_job_cancelled(sync_result.job_tracker_id):
                sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
                sync_result.finish()
                print(f"[GitLabSync] {sync_result}")
                return

            processed_count += 1
            pipeline_id: int | None = pipeline_dict.get("id")

            if pipeline_id is None:
                sync_result.add_skip()
                continue

            try:
                pipeline, created = GitLabSyncPipeline.objects.get_or_create(
                    id=pipeline_id
                )

                # Check if we need to update (compare updated_at from GitLab with our last_synced_at)
                pipeline_updated_at = convert_and_enforce_utc_timezone(
                    datetime_string=pipeline_dict.get("updated_at")
                )

                needs_update = created or (
                    pipeline.last_synced_at is None
                    or (
                        pipeline_updated_at
                        and pipeline_updated_at > pipeline.last_synced_at
                    )
                )

                if not needs_update:
                    sync_result.add_skip()
                    sync_result.update_progress(
                        processed_count,
                        estimated_total,
                        f"⊘ Skipped unchanged pipeline #{pipeline_id}",
                    )
                    continue

                # Update pipeline fields
                pipeline.project = GitLabSyncProject.objects.filter(
                    id=project.id
                ).first()

                user_dict = pipeline_dict.get("user")
                if user_dict:
                    user = GitLabSyncUser.objects.filter(id=user_dict.get("id")).first()
                    if user:
                        pipeline.user = user

                pipeline.sha = pipeline_dict.get("sha")
                pipeline.ref = pipeline_dict.get("ref")
                pipeline.status = pipeline_dict.get("status")
                pipeline.source = pipeline_dict.get("source")
                pipeline.web_url = pipeline_dict.get("web_url")
                pipeline.duration = pipeline_dict.get("duration")
                pipeline.queued_duration = pipeline_dict.get("queued_duration")
                pipeline.coverage = pipeline_dict.get("coverage")
                pipeline.name = pipeline_dict.get("name")
                pipeline.yaml_errors = pipeline_dict.get("yaml_errors")

                pipeline.created_at = convert_and_enforce_utc_timezone(
                    datetime_string=pipeline_dict.get("created_at")
                )
                pipeline.updated_at = pipeline_updated_at
                pipeline.started_at = convert_and_enforce_utc_timezone(
                    datetime_string=pipeline_dict.get("started_at")
                )
                pipeline.finished_at = convert_and_enforce_utc_timezone(
                    datetime_string=pipeline_dict.get("finished_at")
                )
                pipeline.last_synced_at = datetime.now()

                pipeline.save()
                sync_result.add_success()
                sync_result.update_progress(
                    processed_count, estimated_total, f"✓ Synced pipeline #{pipeline_id}"
                )

            except Exception as error:
                error_msg = f"Failed to save pipeline {pipeline_id}: {str(error)}"
                sync_result.add_failure(error_msg)
                sync_result.add_log(f"❌ {error_msg}")
                continue

        # Update estimate based on actual pipelines found
        estimated_total = max(
            estimated_total, processed_count + (project_count - proj_idx) * 5
        )

    sync_result.add_log(
        f"✓ Sync complete: {sync_result.synced_count} synced, "
        f"{sync_result.skipped_count} skipped, {sync_result.failed_count} failed"
    )
    sync_result.finish()
    print(f"[GitLabSync] {sync_result}")


def gitlab_sync_pipelines_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Sync CI/CD pipelines from GitLab EE 17.11.6 with background job tracking.

    New functionality not present in the original git_lab app.
    Tracks pipeline executions for build/test/deploy monitoring.

    Returns immediately with job_id for progress tracking.
    """
    job_tracker = run_sync_in_background("pipelines", _sync_pipelines_background, request)

    return JsonResponse(
        data={"success": True, "job_id": job_tracker.id, "job_type": "pipelines"}
    )
