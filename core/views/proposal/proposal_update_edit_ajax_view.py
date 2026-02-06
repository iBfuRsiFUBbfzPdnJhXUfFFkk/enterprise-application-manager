import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from core.models.proposal_update import ProposalUpdate


@require_http_methods(["POST"])
def proposal_update_edit_ajax_view(request: HttpRequest, update_id: int) -> HttpResponse:
    """Edit a proposal update via AJAX."""
    try:
        update = ProposalUpdate.objects.get(id=update_id)

        data = json.loads(request.body)
        comment_text = data.get("comment", "").strip()
        is_internal = data.get("is_internal_note", False)

        if not comment_text:
            return JsonResponse({"success": False, "error": "Comment text is required"}, status=400)

        update.comment = comment_text
        update.is_internal_note = is_internal
        update.save()

        documents_data = [{
            "id": doc.id,
            "name": doc.name,
            "url": doc.get_file_url(),
            "detail_url": reverse("document_detail", kwargs={"model_id": doc.id}),
            "extension": doc.get_file_extension(),
            "is_image": doc.is_image,
            "thumbnail_url": doc.get_thumbnail_url(),
        } for doc in update.documents.all()]

        response_data = {
            "success": True,
            "update": {
                "id": update.id,
                "author": str(update.person_author) if update.person_author else "Unknown",
                "comment": update.comment,
                "datetime_created": update.datetime_created.strftime("%Y-%m-%d %H:%M"),
                "is_internal_note": update.is_internal_note,
                "documents": documents_data,
            }
        }

        return JsonResponse(response_data)

    except ProposalUpdate.DoesNotExist:
        return JsonResponse({"success": False, "error": "Update not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
