from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from core.models.proposal_update import ProposalUpdate


@require_http_methods(["POST"])
def proposal_update_delete_ajax_view(request: HttpRequest, update_id: int) -> HttpResponse:
    """Delete a proposal update via AJAX."""
    try:
        update = ProposalUpdate.objects.get(id=update_id)
        update.delete()

        return JsonResponse({"success": True})

    except ProposalUpdate.DoesNotExist:
        return JsonResponse({"success": False, "error": "Update not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
