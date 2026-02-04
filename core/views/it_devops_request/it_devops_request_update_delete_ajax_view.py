from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from core.models.it_devops_request_update import ITDevOpsRequestUpdate


@require_http_methods(["POST"])
def it_devops_request_update_delete_ajax_view(request: HttpRequest, update_id: int) -> HttpResponse:
    """Delete an IT/DevOps request update via AJAX."""
    try:
        update = ITDevOpsRequestUpdate.objects.get(id=update_id)
        update.delete()

        return JsonResponse({"success": True})

    except ITDevOpsRequestUpdate.DoesNotExist:
        return JsonResponse({"success": False, "error": "Update not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
