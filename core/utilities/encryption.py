import hashlib
import logging
from os import getenv

from cryptography.fernet import Fernet, InvalidToken

# Configure logger
logger = logging.getLogger(__name__)

# Custom Exception Classes
class EncryptionError(Exception):
    """Base exception for encryption-related errors"""
    pass


class DecryptionFailureError(EncryptionError):
    """Exception raised when decryption fails"""
    pass


class InvalidEncryptionKeyError(DecryptionFailureError):
    """Exception raised when the encryption key is invalid or wrong"""
    pass


class CorruptedDataError(DecryptionFailureError):
    """Exception raised when encrypted data is corrupted"""
    pass


# Initialize cipher suite
secret_key: str | None = getenv('ENCRYPTION_SECRET')
if secret_key is None:
    raise ValueError("ENCRYPTION_SECRET environment variable not set.")
cipher_suite: Fernet = Fernet(key=secret_key.encode())


# Helper Functions
def _compute_validation_hash(plaintext: str) -> str:
    """
    Compute SHA256 hash of plaintext and return first 8 characters.
    Used for validating decryption correctness.
    """
    hash_object = hashlib.sha256(plaintext.encode())
    return hash_object.hexdigest()[:8]


def _format_encrypted_value(encrypted_b64: str, plaintext: str) -> str:
    """
    Format encrypted value with v1 prefix: v1:{hash}:{encrypted_data}
    """
    validation_hash = _compute_validation_hash(plaintext)
    return f"v1:{validation_hash}:{encrypted_b64}"


def _parse_encrypted_value(value: str) -> tuple[str, str, str]:
    """
    Parse encrypted value and return (version, hash, encrypted_data).
    Raises ValueError if format is invalid.
    """
    parts = value.split(':', 2)
    if len(parts) != 3:
        raise ValueError(f"Invalid v1 format: expected 3 parts separated by ':', got {len(parts)}")
    version, validation_hash, encrypted_data = parts
    return version, validation_hash, encrypted_data


def detect_encryption_format(encrypted_value: str) -> str:
    """
    Detect encryption format: 'v1' or 'legacy'.
    Returns 'v1' if value starts with 'v1:', otherwise 'legacy'.
    """
    if encrypted_value.startswith('v1:'):
        return 'v1'
    return 'legacy'


def is_encrypted_value_valid(encrypted_value: str) -> bool:
    """
    Validate encrypted value format without decrypting.
    Returns True if format is valid (v1 or legacy), False otherwise.
    """
    if not encrypted_value:
        return False

    format_type = detect_encryption_format(encrypted_value)

    if format_type == 'v1':
        try:
            _parse_encrypted_value(encrypted_value)
            return True
        except ValueError:
            return False

    # Legacy format - assume valid if non-empty
    return True


def validate_encrypted_data(encrypted_value: str, raise_on_error: bool = False) -> dict:
    """
    Validate encrypted data and return detailed status.

    Args:
        encrypted_value: The encrypted string to validate
        raise_on_error: If True, raise exceptions on validation failure

    Returns:
        dict with keys: 'valid', 'format', 'error'
    """
    result = {
        'valid': False,
        'format': None,
        'error': None
    }

    if not encrypted_value:
        result['error'] = 'Empty or None value'
        if raise_on_error:
            raise CorruptedDataError(result['error'])
        return result

    format_type = detect_encryption_format(encrypted_value)
    result['format'] = format_type

    if format_type == 'v1':
        try:
            _parse_encrypted_value(encrypted_value)
            result['valid'] = True
        except ValueError as e:
            result['error'] = str(e)
            if raise_on_error:
                raise CorruptedDataError(f"Invalid v1 format: {e}")
    else:
        # Legacy format - assume valid
        result['valid'] = True

    return result


# Main Encryption Functions
def encrypt_secret(secret: str | None) -> str | None:
    """
    Encrypt a secret using Fernet encryption with v1 validation format.

    Format: v1:{sha256_hash[:8]}:{fernet_encrypted_base64}

    Args:
        secret: Plaintext secret to encrypt

    Returns:
        Encrypted string in v1 format, or None if input is None
    """
    if secret is None:
        logger.debug("encrypt_secret: Input is None, returning None")
        return None

    if secret == "" or (isinstance(secret, str) and secret.strip() == ""):
        logger.debug("encrypt_secret: Input is empty string, returning None")
        return None

    try:
        # Encrypt with Fernet
        encrypted_bytes: bytes = cipher_suite.encrypt(data=secret.encode())
        encrypted_b64: str = encrypted_bytes.decode()

        # Format with v1 prefix and validation hash
        formatted_value = _format_encrypted_value(encrypted_b64, secret)

        logger.info(f"Successfully encrypted value (v1 format, length={len(formatted_value)})")
        return formatted_value

    except Exception as e:
        logger.error(f"Encryption failed: {e}")
        raise EncryptionError(f"Failed to encrypt secret: {e}")


def decrypt_secret(encrypted_secret: str | None) -> str | None:
    """
    Decrypt a secret, supporting both v1 (with validation) and legacy formats.

    Args:
        encrypted_secret: Encrypted string (v1 or legacy format)

    Returns:
        Decrypted plaintext string, or None if input is None

    Raises:
        InvalidEncryptionKeyError: If decryption fails due to wrong key or validation mismatch
        CorruptedDataError: If data format is corrupted
    """
    if encrypted_secret is None:
        logger.debug("decrypt_secret: Input is None, returning None")
        return None

    if encrypted_secret == "" or (isinstance(encrypted_secret, str) and encrypted_secret.strip() == ""):
        logger.debug("decrypt_secret: Input is empty string, returning None")
        return None

    format_type = detect_encryption_format(encrypted_secret)

    try:
        if format_type == 'v1':
            # Parse v1 format
            version, stored_hash, encrypted_data = _parse_encrypted_value(encrypted_secret)

            # Decrypt the data
            try:
                decrypted_bytes: bytes = cipher_suite.decrypt(token=encrypted_data.encode())
                plaintext: str = decrypted_bytes.decode()
            except InvalidToken as e:
                logger.error(f"Decryption failed (v1 format): Invalid token - likely wrong encryption key")
                raise InvalidEncryptionKeyError(
                    "Failed to decrypt data. The ENCRYPTION_SECRET may be incorrect or the data is corrupted."
                ) from e

            # Validate hash
            computed_hash = _compute_validation_hash(plaintext)
            if computed_hash != stored_hash:
                logger.error(
                    f"Decryption validation failed (v1 format): Hash mismatch. "
                    f"Stored={stored_hash}, Computed={computed_hash}"
                )
                raise InvalidEncryptionKeyError(
                    "Decryption validation failed. The ENCRYPTION_SECRET is likely incorrect."
                )

            logger.debug(f"Successfully decrypted v1 format (length={len(plaintext)})")
            return plaintext

        else:
            # Legacy format - decrypt directly
            try:
                decrypted_bytes: bytes = cipher_suite.decrypt(token=encrypted_secret.encode())
                plaintext: str = decrypted_bytes.decode()
                logger.warning(
                    f"Decrypted legacy format (length={len(plaintext)}). "
                    "Consider re-encrypting to v1 format for enhanced validation."
                )
                return plaintext
            except InvalidToken as e:
                logger.error(f"Decryption failed (legacy format): Invalid token - likely wrong encryption key")
                raise InvalidEncryptionKeyError(
                    "Failed to decrypt data. The ENCRYPTION_SECRET may be incorrect."
                ) from e

    except (InvalidEncryptionKeyError, CorruptedDataError):
        # Re-raise our custom exceptions
        raise
    except ValueError as e:
        # Format parsing error
        logger.error(f"Data format error: {e}")
        raise CorruptedDataError(f"Encrypted data format is invalid: {e}") from e
    except Exception as e:
        # Unexpected error
        logger.error(f"Unexpected decryption error: {e}")
        raise DecryptionFailureError(f"Unexpected error during decryption: {e}") from e
