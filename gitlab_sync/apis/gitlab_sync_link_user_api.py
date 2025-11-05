import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from core.models.person import Person
from gitlab_sync.models import GitLabSyncUser


@csrf_exempt
@require_http_methods(["POST"])
def gitlab_sync_link_user_api(
    request: HttpRequest,
) -> JsonResponse | HttpResponse:
    """
    Link or unlink a GitLab user to a Person record.

    Expected POST data:
    {
        "gitlab_user_id": int,
        "person_id": int | null (null to unlink)
    }
    """
    try:
        data = json.loads(request.body)
        gitlab_user_id = data.get("gitlab_user_id")
        person_id = data.get("person_id")

        if not gitlab_user_id:
            return JsonResponse(
                data={"success": False, "error": "gitlab_user_id is required"},
                status=400,
            )

        gitlab_user = GitLabSyncUser.objects.filter(id=gitlab_user_id).first()
        if not gitlab_user:
            return JsonResponse(
                data={"success": False, "error": "GitLab user not found"}, status=404
            )

        if person_id:
            person = Person.objects.filter(id=person_id).first()
            if not person:
                return JsonResponse(
                    data={"success": False, "error": "Person not found"}, status=404
                )
            gitlab_user.person = person
            action = "linked"
        else:
            gitlab_user.person = None
            action = "unlinked"

        gitlab_user.save()

        return JsonResponse(
            data={
                "success": True,
                "action": action,
                "gitlab_user_id": gitlab_user_id,
                "person_id": person_id,
                "gitlab_username": gitlab_user.username,
                "person_name": (
                    gitlab_user.person.full_name_for_human
                    if gitlab_user.person
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
