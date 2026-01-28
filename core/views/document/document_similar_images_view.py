from typing import Any, Mapping

from django.http import HttpRequest, HttpResponse

from core.models.document import Document
from core.utilities.base_render import base_render
from core.utilities.image_similarity import hamming_distance, similarity_percentage


def document_similar_images_view(request: HttpRequest) -> HttpResponse:
    """Show groups of similar images based on perceptual hash."""
    threshold = int(request.GET.get('threshold', 25))  # Default threshold

    # Get all images with hashes
    images = list(Document.objects.filter(
        image_hash__isnull=False
    ).exclude(image_hash='').order_by('-uploaded_at'))

    # Find similar image groups
    processed_ids = set()
    similar_groups = []

    for img in images:
        if img.id in processed_ids:
            continue

        # Find all images similar to this one
        group = [{
            'document': img,
            'distance': 0,
            'similarity': 100.0,
        }]
        processed_ids.add(img.id)

        for other in images:
            if other.id in processed_ids:
                continue

            distance = hamming_distance(img.image_hash, other.image_hash)
            if 0 <= distance <= threshold:
                similarity = similarity_percentage(img.image_hash, other.image_hash)
                group.append({
                    'document': other,
                    'distance': distance,
                    'similarity': similarity,
                })
                processed_ids.add(other.id)

        # Only include groups with more than one image
        if len(group) > 1:
            # Sort by distance (most similar first)
            group.sort(key=lambda x: x['distance'])
            similar_groups.append({
                'images': group,
                'count': len(group),
            })

    # Sort groups by size (largest first)
    similar_groups.sort(key=lambda x: x['count'], reverse=True)

    context: Mapping[str, Any] = {
        'similar_groups': similar_groups,
        'total_groups': len(similar_groups),
        'total_similar': sum(g['count'] for g in similar_groups),
        'threshold': threshold,
    }

    return base_render(
        context=context,
        request=request,
        template_name='authenticated/document/document_similar_images.html'
    )
