from typing import Any, Mapping

from django.db.models import Count
from django.http import HttpRequest, HttpResponse

from core.models.document import Document
from core.utilities.base_render import base_render


def document_duplicates_view(request: HttpRequest) -> HttpResponse:
    """Show groups of duplicate documents based on file hash with their relations."""
    # Find hashes that appear more than once
    duplicate_hashes = Document.objects.filter(
        file_hash__isnull=False
    ).values('file_hash').annotate(
        count=Count('id')
    ).filter(count__gt=1).order_by('-count')

    # Build list of duplicate groups with relation info
    duplicate_groups = []
    for item in duplicate_hashes:
        documents = Document.objects.filter(
            file_hash=item['file_hash']
        ).prefetch_related(
            'applications',
            'evidence_for_bad_interactions',
            'attachment_for_bad_interaction_updates',
            'attachment_for_hr_incident_updates',
        ).order_by('uploaded_at')

        # Add relation counts to each document
        docs_with_relations = []
        for doc in documents:
            docs_with_relations.append({
                'document': doc,
                'app_count': doc.applications.count(),
                'bad_interaction_count': doc.evidence_for_bad_interactions.count(),
                'bad_interaction_update_count': doc.attachment_for_bad_interaction_updates.count(),
                'hr_incident_update_count': doc.attachment_for_hr_incident_updates.count(),
                'total_relations': (
                    doc.applications.count() +
                    doc.evidence_for_bad_interactions.count() +
                    doc.attachment_for_bad_interaction_updates.count() +
                    doc.attachment_for_hr_incident_updates.count()
                ),
            })

        duplicate_groups.append({
            'hash': item['file_hash'],
            'count': item['count'],
            'documents': docs_with_relations,
        })

    context: Mapping[str, Any] = {
        'duplicate_groups': duplicate_groups,
        'total_duplicates': sum(g['count'] - 1 for g in duplicate_groups),
        'total_groups': len(duplicate_groups),
    }

    return base_render(
        context=context,
        request=request,
        template_name='authenticated/document/document_duplicates.html'
    )
