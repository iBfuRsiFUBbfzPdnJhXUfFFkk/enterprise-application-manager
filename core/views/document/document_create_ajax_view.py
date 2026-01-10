from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from core.forms.document_form import DocumentForm


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def document_create_ajax_view(request: HttpRequest) -> JsonResponse:
    """
    AJAX endpoint for creating a new document/attachment from a modal.
    Handles file uploads and returns JSON with the newly created document data or validation errors.
    """
    try:
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            document = form.save()

            return JsonResponse({
                'success': True,
                'document': {
                    'id': document.id,
                    'name': document.name,
                    'version': document.version or '',
                    'comment': document.comment or '',
                    'filename': document.get_filename() or '',
                    'file_size': document.get_file_size() or 0,
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'errors': {'_all': [str(e)]}
        }, status=500)
