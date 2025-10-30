import random
import string


# Reserved short codes that cannot be used (to avoid conflicts with existing routes)
RESERVED_SHORT_CODES = {
    'admin',
    'api',
    'authenticated',
    'static',
    'media',
    'login',
    'logout',
    'health',
    'new',
    'edit',
    'delete',
    'create',
    'update',
    'list',
    'detail',
    'view',
}


def generate_short_code(length: int = 10, max_attempts: int = 10) -> str:
    """
    Generate a random alphanumeric short code.

    Args:
        length: Length of the short code (default: 10 characters)
        max_attempts: Maximum number of attempts to generate a unique code

    Returns:
        A random alphanumeric string of specified length

    Raises:
        ValueError: If unable to generate a non-reserved code after max_attempts
    """
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits

    for attempt in range(max_attempts):
        short_code = ''.join(random.choice(characters) for _ in range(length))

        # Check if it's not a reserved word
        if short_code.lower() not in RESERVED_SHORT_CODES:
            return short_code

    raise ValueError(f"Unable to generate non-reserved short code after {max_attempts} attempts")


def generate_unique_short_code(
    model_class,
    field_name: str = 'short_code',
    length: int = 10,
    max_attempts: int = 100
) -> str:
    """
    Generate a unique short code that doesn't exist in the database.

    Args:
        model_class: The Django model class to check against
        field_name: The field name to check for uniqueness (default: 'short_code')
        length: Length of the short code (default: 10 characters)
        max_attempts: Maximum number of attempts to find a unique code

    Returns:
        A unique random alphanumeric string

    Raises:
        ValueError: If unable to generate a unique code after max_attempts
    """
    from django.db.models import Q

    for attempt in range(max_attempts):
        short_code = generate_short_code(length=length)

        # Check if this code already exists in the database
        filter_kwargs = {f"{field_name}__iexact": short_code}
        if not model_class.objects.filter(**filter_kwargs).exists():
            return short_code

    raise ValueError(f"Unable to generate unique short code after {max_attempts} attempts")


def validate_short_code(short_code: str) -> tuple[bool, str | None]:
    """
    Validate a user-provided short code.

    Args:
        short_code: The short code to validate

    Returns:
        Tuple of (is_valid, error_message)
        If valid, error_message is None
        If invalid, error_message contains the reason
    """
    if not short_code:
        return False, "Short code cannot be empty"

    if len(short_code) > 50:
        return False, "Short code must be 50 characters or less"

    if not short_code.replace('_', '').replace('-', '').isalnum():
        return False, "Short code can only contain letters, numbers, hyphens, and underscores"

    if short_code.lower() in RESERVED_SHORT_CODES:
        return False, f"'{short_code}' is a reserved word and cannot be used"

    return True, None
