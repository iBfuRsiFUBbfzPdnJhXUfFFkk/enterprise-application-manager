import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from core.models.application import Application
from gitlab_sync.models import GitLabSyncProject


@csrf_exempt
@require_http_methods(["POST"])
def gitlab_sync_link_project_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Link or unlink a GitLab project to an Application record.

    Expected POST data:
    {
        "gitlab_project_id": int,
        "application_id": int | null (null to unlink)
    }
    """
    try:
        data = json.loads(request.body)
        gitlab_project_id = data.get("gitlab_project_id")
        application_id = data.get("application_id")

        if not gitlab_project_id:
            return JsonResponse(
                data={"success": False, "error": "gitlab_project_id is required"},
                status=400,
            )

        gitlab_project = GitLabSyncProject.objects.filter(id=gitlab_project_id).first()
        if not gitlab_project:
            return JsonResponse(
                data={"success": False, "error": "GitLab project not found"}, status=404
            )

        if application_id:
            application = Application.objects.filter(id=application_id).first()
            if not application:
                return JsonResponse(
                    data={"success": False, "error": "Application not found"},
                    status=404,
                )
            gitlab_project.application = application
            action = "linked"
        else:
            gitlab_project.application = None
            action = "unlinked"

        gitlab_project.save()

        return JsonResponse(
            data={
                "success": True,
                "action": action,
                "gitlab_project_id": gitlab_project_id,
                "application_id": application_id,
                "gitlab_project_name": gitlab_project.path_with_namespace,
                "application_name": (
                    gitlab_project.application.name
                    if gitlab_project.application
                    else None
                ),
            }
        )

    except json.JSONDecodeError:
        return JsonResponse(
            data={"success": False, "error": "Invalid JSON"}, status=400
        )
    except Exception as error:
        return JsonResponse(
            data={"success": False, "error": str(error)}, status=500
        )
