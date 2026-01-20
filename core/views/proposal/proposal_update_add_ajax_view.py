import json
from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from core.models.proposal import Proposal
from core.models.proposal_update import ProposalUpdate
from core.utilities.get_user_from_request import get_user_from_request


@require_http_methods(["POST"])
def proposal_update_add_ajax_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """Add an update to a proposal via AJAX."""
    try:
        proposal = Proposal.objects.get(id=model_id)

        data = json.loads(request.body)
        comment_text = data.get("comment", "").strip()
        is_internal = data.get("is_internal_note", False)

        if not comment_text:
            return JsonResponse({"success": False, "error": "Comment text is required"}, status=400)

        user = get_user_from_request(request=request)
        person = None
        if user and hasattr(user, 'person_mapping') and user.person_mapping:
            person = user.person_mapping

        if not person:
            return JsonResponse({"success": False, "error": "Current user has no person mapping"}, status=400)

        update = ProposalUpdate.objects.create(
            proposal=proposal,
            person_author=person,
            comment=comment_text,
            is_internal_note=is_internal,
        )

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

    except Proposal.DoesNotExist:
        return JsonResponse({"success": False, "error": "Proposal not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
