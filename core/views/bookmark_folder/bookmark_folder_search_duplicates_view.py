from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods

from core.models.bookmark_folder import BookmarkFolder


@login_required
@require_http_methods(["GET"])
def bookmark_folder_search_duplicates_view(request: HttpRequest) -> JsonResponse:
    """
    AJAX endpoint for searching folders with similar names for duplicate detection.
    Checks both for exact conflicts (same name in same parent) and similar names.
    """
    name = request.GET.get('name', '').strip()
    parent_id = request.GET.get('parent_id')
    exclude_id = request.GET.get('exclude_id')

    if not name or len(name) < 2:
        return JsonResponse({'exact_conflict': False, 'similar': []})

    queryset = BookmarkFolder.objects.filter(user=request.user)

    if exclude_id:
        try:
            queryset = queryset.exclude(id=int(exclude_id))
        except (ValueError, TypeError):
            pass

    parent = None
    if parent_id:
        try:
            parent = BookmarkFolder.objects.filter(id=int(parent_id), user=request.user).first()
        except (ValueError, TypeError):
            pass

    exact_conflict = queryset.filter(name__iexact=name, parent_folder=parent).exists()

    similar_folders = queryset.filter(name__icontains=name)[:5]
    similar = []
    for folder in similar_folders:
        path = ' / '.join([f.name for f in folder.get_breadcrumb])
        similar.append({
            'id': folder.id,
            'name': folder.name,
            'path': path
        })

    return JsonResponse({
        'exact_conflict': exact_conflict,
        'similar': similar
    })
