import json
from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from core.models.it_devops_request import ITDevOpsRequest
from core.models.it_devops_request_update import ITDevOpsRequestUpdate
from core.utilities.get_user_from_request import get_user_from_request


@require_http_methods(["POST"])
def it_devops_request_update_add_ajax_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """Add an update to an IT/DevOps request via AJAX."""
    try:
        # Get the request
        it_devops_request = ITDevOpsRequest.objects.get(id=model_id)

        # Parse JSON body
        data = json.loads(request.body)
        comment_text = data.get("comment", "").strip()
        is_internal = data.get("is_internal_note", False)

        if not comment_text:
            return JsonResponse({"success": False, "error": "Comment text is required"}, status=400)

        # Get the current user's person mapping
        user = get_user_from_request(request=request)
        person = None
        if user and hasattr(user, 'person_mapping') and user.person_mapping:
            person = user.person_mapping

        if not person:
            return JsonResponse({"success": False, "error": "Current user has no person mapping"}, status=400)

        # Create the update
        update = ITDevOpsRequestUpdate.objects.create(
            it_devops_request=it_devops_request,
            person_author=person,
            comment=comment_text,
            is_internal_note=is_internal,
        )

        # Return success with update data
        response_data: Mapping[str, Any] = {
            "success": True,
            "update": {
                "id": update.id,
                "author": str(person),
                "comment": update.comment,
                "datetime_created": update.datetime_created.strftime("%Y-%m-%d %H:%M:%S"),
                "is_internal_note": update.is_internal_note,
            }
        }

        return JsonResponse(response_data)

    except ITDevOpsRequest.DoesNotExist:
        return JsonResponse({"success": False, "error": "Request not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
