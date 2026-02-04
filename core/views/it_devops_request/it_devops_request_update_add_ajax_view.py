import json
from typing import Any

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from core.models.document import Document
from core.models.it_devops_request import ITDevOpsRequest
from core.models.it_devops_request_update import ITDevOpsRequestUpdate
from core.utilities.get_user_from_request import get_user_from_request


@require_http_methods(["POST"])
def it_devops_request_update_add_ajax_view(request: HttpRequest, model_id: int) -> HttpResponse:
    """Add an update to an IT/DevOps request via AJAX."""
    try:
        it_devops_request = ITDevOpsRequest.objects.get(id=model_id)

        # Check if this is a multipart form (with files) or JSON
        content_type = request.content_type or ''
        if 'multipart/form-data' in content_type:
            comment_text = request.POST.get("comment", "").strip()
            is_internal = request.POST.get("is_internal_note") == "true"
            files = request.FILES.getlist("documents")
        else:
            data = json.loads(request.body)
            comment_text = data.get("comment", "").strip()
            is_internal = data.get("is_internal_note", False)
            files = []

        if not comment_text:
            return JsonResponse({"success": False, "error": "Comment text is required"}, status=400)

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

        # Handle file uploads
        documents_data = []
        for uploaded_file in files:
            doc = Document.objects.create(
                name=uploaded_file.name,
                file=uploaded_file,
                version="1.0",
            )
            update.documents.add(doc)
            documents_data.append({
                "id": doc.id,
                "name": doc.name,
                "url": doc.get_file_url(),
                "extension": doc.get_file_extension(),
            })

        response_data: dict[str, Any] = {
            "success": True,
            "update": {
                "id": update.id,
                "author": str(person),
                "comment": update.comment,
                "datetime_created": update.datetime_created.strftime("%Y-%m-%d %H:%M"),
                "is_internal_note": update.is_internal_note,
                "documents": documents_data,
            }
        }

        return JsonResponse(response_data)

    except ITDevOpsRequest.DoesNotExist:
        return JsonResponse({"success": False, "error": "Request not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)
