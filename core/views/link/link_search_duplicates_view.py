from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from core.models.link import Link


@login_required
@require_http_methods(["GET"])
def link_search_duplicates_view(request: HttpRequest) -> JsonResponse:
    """
    AJAX endpoint for searching links with similar name or URL.
    Used for duplicate detection during link creation/editing.
    """
    name = request.GET.get('name', '').strip()
    url = request.GET.get('url', '').strip()
    exclude_id = request.GET.get('exclude_id')

    duplicates = []
    seen_ids = set()

    queryset = Link.objects.all()
    if exclude_id:
        try:
            queryset = queryset.exclude(id=int(exclude_id))
        except (ValueError, TypeError):
            pass

    if name and len(name) >= 2:
        name_matches = queryset.filter(name__icontains=name)[:5]
        for link in name_matches:
            if link.id not in seen_ids:
                seen_ids.add(link.id)
                duplicates.append({
                    'id': link.id,
                    'name': link.name,
                    'url': link.url,
                    'match_type': 'name'
                })

    if url and len(url) >= 5:
        normalized_url = url.lower().replace('https://', '').replace('http://', '').rstrip('/')
        url_matches = queryset.filter(url__icontains=normalized_url)[:5]
        for link in url_matches:
            if link.id not in seen_ids:
                seen_ids.add(link.id)
                duplicates.append({
                    'id': link.id,
                    'name': link.name,
                    'url': link.url,
                    'match_type': 'url'
                })

    return JsonResponse({'duplicates': duplicates[:10]})
