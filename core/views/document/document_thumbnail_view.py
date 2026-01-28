from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from core.models.document import Document
import boto3
from django.conf import settings


@login_required
def document_thumbnail_view(request, model_id):
    """Serve document thumbnail through authenticated Django view."""
    document = get_object_or_404(Document, pk=model_id)

    if not document.has_thumbnail:
        raise Http404("Thumbnail not found")

    # Get file from MinIO using boto3 with server credentials
    s3_client = boto3.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    # Get thumbnail from MinIO
    file_obj = s3_client.get_object(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Key=document.thumbnail.name
    )

    # Stream file to response with long cache (thumbnails don't change)
    response = FileResponse(
        file_obj['Body'],
        content_type='image/avif'
    )
    response['Cache-Control'] = 'public, max-age=31536000'

    return response
