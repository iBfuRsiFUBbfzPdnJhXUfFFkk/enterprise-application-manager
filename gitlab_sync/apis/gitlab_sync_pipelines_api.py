from typing import cast

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from gitlab import Gitlab
from gitlab.v4.objects import Project, ProjectPipeline

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
from gitlab_sync.models import GitLabSyncPipeline, GitLabSyncProject, GitLabSyncUser
from gitlab_sync.utilities import SyncResult, handle_gitlab_api_errors


def gitlab_sync_pipelines_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Sync CI/CD pipelines from GitLab EE 17.11.6 with improved error handling.

    New functionality not present in the original git_lab app.
    Tracks pipeline executions for build/test/deploy monitoring.
    """
    sync_result = SyncResult(entity_type="GitLabSyncPipeline")

    query_parameters: GitLabApiCommonQueryParameters = get_common_query_parameters(
        request=request
    )

    git_lab_client: Gitlab | None = get_git_lab_client()
    if git_lab_client is None:
        sync_result.add_failure("Failed to get GitLab client")
        sync_result.finish()
        print(f"[GitLabSync] {sync_result}")
        return generic_500(request=request)

    projects: QuerySet[GitLabSyncProject] = cast_query_set(
        typ=GitLabSyncProject,
        val=GitLabSyncProject.objects.all(),
    )

    all_pipelines: list[dict] = []

    for project in projects:
        pipelines, error = handle_gitlab_api_errors(
            func=lambda: [
                p.asdict()
                for p in cast(
                    list[ProjectPipeline],
                    git_lab_client.projects.get(id=project.id, lazy=True)
                    .pipelines.list(**query_parameters),
                )
            ],
            entity_name=f"Pipelines for project {project.path_with_namespace}",
            max_retries=3,
        )

        if error:
            sync_result.add_failure(error)
            continue

        if pipelines:
            for pipeline in pipelines:
                pipeline["_project_id"] = project.id
            all_pipelines.extend(pipelines)

    for pipeline_dict in all_pipelines:
        pipeline_id: int | None = pipeline_dict.get("id")
        if pipeline_id is None:
            sync_result.add_skip()
            continue

        try:
            pipeline, created = GitLabSyncPipeline.objects.get_or_create(id=pipeline_id)

            project_id = pipeline_dict.get("_project_id")
            if project_id:
                pipeline.project = GitLabSyncProject.objects.filter(
                    id=project_id
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
            pipeline.updated_at = convert_and_enforce_utc_timezone(
                datetime_string=pipeline_dict.get("updated_at")
            )
            pipeline.started_at = convert_and_enforce_utc_timezone(
                datetime_string=pipeline_dict.get("started_at")
            )
            pipeline.finished_at = convert_and_enforce_utc_timezone(
                datetime_string=pipeline_dict.get("finished_at")
            )

            pipeline.save()
            sync_result.add_success()

        except Exception as error:
            error_msg = f"Failed to save pipeline {pipeline_id}: {str(error)}"
            sync_result.add_failure(error_msg)
            continue

    sync_result.finish()
    print(f"[GitLabSync] {sync_result}")

    return JsonResponse(data=sync_result.to_dict(), safe=False)
