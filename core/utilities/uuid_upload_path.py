import uuid


def uuid_upload_path(instance, filename: str) -> str:
    """
    Generate a UUID-based file path for uploads.
    Preserves the original file extension.
    """
    extension = ''
    if '.' in filename:
        extension = '.' + filename.rsplit('.', 1)[-1]
    return f"documents/{uuid.uuid4()}{extension}"
