from django.contrib.auth.backends import BaseBackend

from core.models.user import User
from core.models.user_passkey import UserPasskey


class PasskeyBackend(BaseBackend):
    """
    Authentication backend for passkey-based login.
    This backend authenticates users based on WebAuthn credential verification.
    """

    def authenticate(self, request, credential_id=None, **kwargs):
        """
        Authenticate user based on verified WebAuthn credential.

        Args:
            request: The HTTP request
            credential_id: The credential ID from verified WebAuthn assertion

        Returns:
            User object if authentication successful, None otherwise
        """
        if credential_id is None:
            return None

        try:
            passkey = UserPasskey.objects.select_related('user').get(credential_id=credential_id)
            return passkey.user
        except UserPasskey.DoesNotExist:
            return None

    def get_user(self, user_id):
        """Get user by ID (required by Django authentication backend interface)."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
