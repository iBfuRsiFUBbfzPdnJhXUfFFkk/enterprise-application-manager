import json
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from core.forms.link_form import LinkForm


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def link_create_ajax_view(request: HttpRequest) -> JsonResponse:
    """
    AJAX endpoint for creating a new link from a modal.
    Returns JSON with the newly created link data or validation errors.
    """
    try:
        data = json.loads(request.body)
        form = LinkForm(data)

        if form.is_valid():
            link = form.save()
            return JsonResponse({
                'success': True,
                'link': {
                    'id': link.id,
                    'name': link.name,
                    'url': link.url,
                    'comment': link.comment or ''
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            }, status=400)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'errors': {'_all': ['Invalid JSON data']}
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'errors': {'_all': [str(e)]}
        }, status=500)
