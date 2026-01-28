import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from core.models.bad_interaction import BadInteraction
from core.models.document import Document


@login_required
@require_POST
def bad_interaction_fix_evidence_view(request, model_id: int):
    """Update evidence document reference to point to an existing document."""
    try:
        bad_interaction = BadInteraction.objects.get(id=model_id)
    except BadInteraction.DoesNotExist:
        return JsonResponse({'error': 'Bad interaction not found'}, status=404)

    try:
        data = json.loads(request.body)
        document_id = data.get('document_id')

        if not document_id:
            return JsonResponse({'error': 'document_id is required'}, status=400)

        # Get the document
        try:
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            return JsonResponse({'error': 'Document not found'}, status=404)

        # Update the evidence document reference
        bad_interaction.evidence_document = document
        bad_interaction.save()

        return JsonResponse({
            'success': True,
            'filename': bad_interaction.get_evidence_filename(),
            'url': bad_interaction.get_evidence_url(),
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
