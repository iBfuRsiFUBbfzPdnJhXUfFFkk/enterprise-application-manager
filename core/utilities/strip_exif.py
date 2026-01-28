import io
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from PIL import Image


IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.tiff', '.tif'}


def strip_exif_from_file(uploaded_file):
    """
    Strip EXIF data from an uploaded image file.
    Returns the processed file or the original if not an image.
    """
    if not uploaded_file:
        return uploaded_file

    filename = uploaded_file.name.lower()
    extension = ''
    if '.' in filename:
        extension = '.' + filename.rsplit('.', 1)[-1]

    if extension not in IMAGE_EXTENSIONS:
        return uploaded_file

    try:
        uploaded_file.seek(0)
        image = Image.open(uploaded_file)

        # Create a new image without EXIF data
        data = list(image.getdata())
        clean_image = Image.new(image.mode, image.size)
        clean_image.putdata(data)

        # Save to buffer
        buffer = io.BytesIO()
        image_format = _get_image_format(extension)
        save_kwargs = {'format': image_format}

        # Preserve quality for JPEG
        if image_format == 'JPEG':
            save_kwargs['quality'] = 95

        clean_image.save(buffer, **save_kwargs)
        buffer.seek(0)

        # Create new uploaded file
        return InMemoryUploadedFile(
            file=buffer,
            field_name=uploaded_file.field_name if hasattr(uploaded_file, 'field_name') else None,
            name=uploaded_file.name,
            content_type=uploaded_file.content_type,
            size=buffer.getbuffer().nbytes,
            charset=None
        )
    except Exception:
        # If processing fails, return original file
        uploaded_file.seek(0)
        return uploaded_file


def _get_image_format(extension: str) -> str:
    """Map file extension to PIL image format."""
    format_map = {
        '.jpg': 'JPEG',
        '.jpeg': 'JPEG',
        '.png': 'PNG',
        '.webp': 'WEBP',
        '.tiff': 'TIFF',
        '.tif': 'TIFF',
    }
    return format_map.get(extension, 'JPEG')
