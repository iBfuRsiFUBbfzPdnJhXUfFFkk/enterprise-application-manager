import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from core.models.it_devops_request_update import ITDevOpsRequestUpdate


@require_http_methods(["POST"])
def it_devops_request_update_edit_ajax_view(request: HttpRequest, update_id: int) -> HttpResponse:
    """Edit an IT/DevOps request update via AJAX."""
    try:
        update = ITDevOpsRequestUpdate.objects.get(id=update_id)

        data = json.loads(request.body)
        comment_text = data.get("comment", "").strip()
        is_internal = data.get("is_internal_note", False)

        if not comment_text:
            return JsonResponse({"success": False, "error": "Comment text is required"}, status=400)

        update.comment = comment_text
        update.is_internal_note = is_internal
        update.save()

        response_data = {
            "success": True,
            "update": {
                "id": update.id,
                "author": str(update.person_author) if update.person_author else "Unknown",
                "comment": update.comment,
                "datetime_created": update.datetime_created.strftime("%Y-%m-%d %H:%M"),
                "is_internal_note": update.is_internal_note,
            }
        }

        return JsonResponse(response_data)

    except ITDevOpsRequestUpdate.DoesNotExist:
        return JsonResponse({"success": False, "error": "Update not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
