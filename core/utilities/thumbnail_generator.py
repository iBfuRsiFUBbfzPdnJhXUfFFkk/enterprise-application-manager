"""Thumbnail generation utility for documents."""
import io
import logging

from django.core.files.uploadedfile import InMemoryUploadedFile

logger = logging.getLogger(__name__)

IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'gif', 'bmp', 'tiff', 'tif'}
THUMBNAIL_MAX_SIZE = (400, 400)
THUMBNAIL_QUALITY = 60


def generate_thumbnail(file_field, filename: str) -> InMemoryUploadedFile | None:
    """
    Generate an AVIF thumbnail for an image or PDF file.

    Args:
        file_field: Django file field (from model.file)
        filename: Original filename to determine file type

    Returns:
        InMemoryUploadedFile containing AVIF thumbnail, or None if generation fails
    """
    if not file_field or not filename:
        return None

    extension = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''

    try:
        if extension in IMAGE_EXTENSIONS:
            return _generate_image_thumbnail(file_field)
        elif extension == 'pdf':
            return _generate_pdf_thumbnail(file_field)
    except Exception as e:
        logger.warning(f"Thumbnail generation failed for {filename}: {e}")

    return None


def _generate_image_thumbnail(file_field) -> InMemoryUploadedFile | None:
    """Generate thumbnail from an image file."""
    import pillow_avif  # noqa: F401 - registers AVIF support
    from PIL import Image

    file_field.seek(0)
    image = Image.open(file_field)

    # Convert to RGB if necessary (AVIF doesn't support all modes)
    if image.mode in ('RGBA', 'P'):
        background = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        background.paste(image, mask=image.split()[3] if len(image.split()) > 3 else None)
        image = background
    elif image.mode != 'RGB':
        image = image.convert('RGB')

    # Create thumbnail maintaining aspect ratio
    image.thumbnail(THUMBNAIL_MAX_SIZE, Image.Resampling.LANCZOS)

    # Save to AVIF format
    output = io.BytesIO()
    image.save(output, format='AVIF', quality=THUMBNAIL_QUALITY)
    output.seek(0)

    return InMemoryUploadedFile(
        file=output,
        field_name='thumbnail',
        name='thumbnail.avif',
        content_type='image/avif',
        size=output.getbuffer().nbytes,
        charset=None
    )


def _generate_pdf_thumbnail(file_field) -> InMemoryUploadedFile | None:
    """Generate thumbnail from first page of PDF."""
    import pillow_avif  # noqa: F401 - registers AVIF support
    from PIL import Image
    from pdf2image import convert_from_bytes

    file_field.seek(0)
    pdf_bytes = file_field.read()

    # Convert first page to image
    images = convert_from_bytes(pdf_bytes, first_page=1, last_page=1, dpi=150)
    if not images:
        return None

    image = images[0]

    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Create thumbnail maintaining aspect ratio
    image.thumbnail(THUMBNAIL_MAX_SIZE, Image.Resampling.LANCZOS)

    # Save to AVIF format
    output = io.BytesIO()
    image.save(output, format='AVIF', quality=THUMBNAIL_QUALITY)
    output.seek(0)

    return InMemoryUploadedFile(
        file=output,
        field_name='thumbnail',
        name='thumbnail.avif',
        content_type='image/avif',
        size=output.getbuffer().nbytes,
        charset=None
    )
