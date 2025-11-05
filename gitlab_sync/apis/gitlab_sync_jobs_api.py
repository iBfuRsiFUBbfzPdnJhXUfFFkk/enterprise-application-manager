from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone
from gitlab import Gitlab

from core.utilities.cast_query_set import cast_query_set
from core.utilities.convert_and_enforce_utc_timezone import (
    convert_and_enforce_utc_timezone,
)
from core.utilities.git_lab.get_git_lab_client import get_git_lab_client
from gitlab_sync.models import (
    GitLabSyncJob,
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


def _sync_jobs_background(
    request: HttpRequest, job_tracker: GitLabSyncJobTracker
) -> None:
    """Background function to sync CI/CD jobs with progress tracking."""
    sync_result = SyncResult(
        entity_type="GitLabSyncJob", job_tracker_id=job_tracker.id
    )
    sync_result.add_log("Starting CI/CD jobs sync...")

    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        sync_result.add_log("❌ Failed to get GitLab client")
        sync_result.add_failure("Failed to get GitLab client")
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return

    pipelines: QuerySet[GitLabSyncPipeline] = cast_query_set(
        typ=GitLabSyncPipeline,
        val=GitLabSyncPipeline.objects.select_related("project").all(),
    )

    pipeline_count = pipelines.count()
    sync_result.add_log(
        f"Syncing jobs from {pipeline_count} pipelines incrementally..."
    )

    for pipe_idx, pipeline in enumerate(pipelines, 1):
        # Check if job was cancelled
        if check_job_cancelled(sync_result.job_tracker_id):
            sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
            sync_result.finish()
            print(f"[GitLabSync] {sync_result}")
            return

        if not pipeline.project:
            sync_result.add_log(f"⚠️ Pipeline {pipeline.id} has no associated project - skipping")
            continue

        # Update progress at pipeline level
        sync_result.update_progress(
            pipe_idx - 1,
            pipeline_count,
            f"📥 About to fetch jobs from pipeline {pipeline.id} in project {pipeline.project.path_with_namespace} (pipeline {pipe_idx}/{pipeline_count})...",
        )

        jobs, error = handle_gitlab_api_errors(
            func=lambda: [
                j.asdict()
                for j in git_lab_client.projects.get(id=pipeline.project.id, lazy=True)
                .pipelines.get(id=pipeline.id, lazy=True)
                .jobs.list(get_all=True)
            ],
            entity_name=f"Jobs for pipeline {pipeline.id}",
            max_retries=3,
        )

        if error:
            # Check if this is a 403 Forbidden error - if so, just log and continue without failing
            error_str = str(error).lower()
            if (
                "403" in error_str
                or "forbidden" in error_str
                or "access denied" in error_str
                or "permission denied" in error_str
            ):
                sync_result.add_log(
                    f"⚠️ Access denied (403) for jobs in pipeline {pipeline.id} - skipping"
                )
                continue

            # For other errors, add as failure
            sync_result.add_log(
                f"❌ Error fetching jobs for pipeline {pipeline.id}: {error}"
            )
            sync_result.add_failure(error)
            continue

        if not jobs:
            sync_result.add_log(f"⊘ No jobs found in pipeline {pipeline.id}")
            continue

        sync_result.add_log(f"✓ Fetched {len(jobs)} jobs from pipeline {pipeline.id}, about to process...")

        # Process each job immediately
        for job_dict in jobs:
            # Check if job was cancelled
            if check_job_cancelled(sync_result.job_tracker_id):
                sync_result.add_log("⚠️ Job cancelled by user, stopping sync...")
                sync_result.finish()
                print(f"[GitLabSync] {sync_result}")
                return

            job_id: int | None = job_dict.get("id")

            if job_id is None:
                sync_result.add_skip()
                continue

            try:
                sync_result.add_log(f"💾 About to get_or_create job {job_id} in database...")
                ci_job, created = GitLabSyncJob.objects.get_or_create(
                    id=job_id
                )
                sync_result.add_log(f"✓ Database get_or_create succeeded for job {job_id} (created={created})")

                # Check if we need to update (compare created_at from GitLab with our last_synced_at)
                job_created_at = convert_and_enforce_utc_timezone(
                    datetime_string=job_dict.get("created_at")
                )

                needs_update = created or (
                    ci_job.last_synced_at is None
                    or (
                        job_created_at
                        and job_created_at > ci_job.last_synced_at
                    )
                )

                if not needs_update:
                    sync_result.add_skip()
                    sync_result.add_log(f"⊘ Skipped unchanged job #{job_id}")
                    continue

                # Update job fields
                ci_job.pipeline = pipeline
                ci_job.project = pipeline.project

                # Handle user
                user_dict = job_dict.get("user")
                if user_dict:
                    user = GitLabSyncUser.objects.filter(id=user_dict.get("id")).first()
                    if user:
                        ci_job.user = user

                ci_job.name = job_dict.get("name")
                ci_job.stage = job_dict.get("stage")
                ci_job.status = job_dict.get("status")
                ci_job.ref = job_dict.get("ref")
                ci_job.tag = job_dict.get("tag")
                ci_job.coverage = job_dict.get("coverage")
                ci_job.allow_failure = job_dict.get("allow_failure")
                ci_job.duration = job_dict.get("duration")
                ci_job.queued_duration = job_dict.get("queued_duration")
                ci_job.failure_reason = job_dict.get("failure_reason")
                ci_job.web_url = job_dict.get("web_url")

                # Handle runner information
                runner_dict = job_dict.get("runner")
                if runner_dict:
                    ci_job.runner_description = runner_dict.get("description")

                ci_job.created_at = job_created_at
                ci_job.started_at = convert_and_enforce_utc_timezone(
                    datetime_string=job_dict.get("started_at")
                )
                ci_job.finished_at = convert_and_enforce_utc_timezone(
                    datetime_string=job_dict.get("finished_at")
                )
                ci_job.last_synced_at = timezone.now()

                sync_result.add_log(f"💾 About to save job {job_id} to database...")
                ci_job.save()
                sync_result.add_log(f"✓ Database save succeeded for job {job_id}")
                sync_result.add_success()

            except Exception as error:
                import traceback
                error_trace = traceback.format_exc()
                error_msg = f"Failed to save job {job_id}: {str(error)}"
                sync_result.add_failure(error_msg)
                sync_result.add_log(f"❌ {error_msg}")
                print(f"[GitLabSync] {error_msg}")
                print(f"[GitLabSync] Stack trace:\n{error_trace}")
                continue

    # Final progress update
    sync_result.update_progress(pipeline_count, pipeline_count, None)

    sync_result.add_log(
        f"✓ Sync complete: {sync_result.synced_count} synced, "
        f"{sync_result.skipped_count} skipped, {sync_result.failed_count} failed"
    )
    sync_result.finish()
    print(f"[GitLabSync] {sync_result}")


def gitlab_sync_jobs_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Sync CI/CD jobs from GitLab EE 17.11.6 with background job tracking.

    New functionality not present in the original git_lab app.
    Tracks individual build/test/deploy jobs within pipelines.

    Returns immediately with job_id for progress tracking.
    """
    job_tracker = run_sync_in_background("jobs", _sync_jobs_background, request)

    return JsonResponse(
        data={"success": True, "job_id": job_tracker.id, "job_type": "jobs"}
    )
