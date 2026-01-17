import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from core.models.link import Link


@csrf_exempt
@login_required
@require_http_methods(["GET", "POST"])
def link_edit_ajax_view(request: HttpRequest, link_id: int) -> JsonResponse:
    """
    AJAX endpoint for editing a link from a modal.
    GET: Returns the link data as JSON.
    POST: Updates the link and returns success/errors.
    """
    try:
        link = Link.objects.get(id=link_id)
    except Link.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Link not found.'
        }, status=404)

    if request.method == 'GET':
        return JsonResponse({
            'success': True,
            'link': {
                'id': link.id,
                'name': link.name,
                'url': link.url,
                'comment': link.comment or ''
            }
        })

    # POST - update link
    try:
        data = json.loads(request.body)

        errors = {}

        name = data.get('name', '').strip()
        if not name:
            errors['name'] = ['Name is required.']

        url = data.get('url', '').strip()
        if not url:
            errors['url'] = ['URL is required.']

        if errors:
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)

        link.name = name
        link.url = url
        link.comment = data.get('comment', '').strip() or None
        link.save()

        return JsonResponse({
            'success': True,
            'link': {
                'id': link.id,
                'name': link.name,
                'url': link.url,
                'comment': link.comment or ''
            }
        })

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
