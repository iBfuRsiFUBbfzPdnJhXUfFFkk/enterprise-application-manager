from django.db import models
from django.utils import timezone
from django_generic_model_fields.create_generic_boolean import create_generic_boolean
from django_generic_model_fields.create_generic_fk import create_generic_fk
from django_generic_model_fields.create_generic_varchar import create_generic_varchar

from core.models.common.abstract.abstract_base_model import AbstractBaseModel


class UserPasskey(AbstractBaseModel):
    """
    Stores WebAuthn passkey credentials for users.
    Each user can have multiple passkeys (different devices).
    """

    user = create_generic_fk(to='core.User', related_name='passkeys')
    name: str = create_generic_varchar()
    credential_id: str = models.TextField(unique=True)
    public_key: str = models.TextField()
    sign_count: int = models.IntegerField(default=0)
    aaguid: str | None = create_generic_varchar()
    credential_type: str = create_generic_varchar()
    transports: str | None = create_generic_varchar()
    backup_eligible: bool = create_generic_boolean(default=False)
    backup_state: bool = create_generic_boolean(default=False)
    user_verified: bool = create_generic_boolean(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    last_used_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

    def update_last_used(self):
        """Update the last_used_at timestamp to now."""
        self.last_used_at = timezone.now()
        self.save(update_fields=['last_used_at'])

    class Meta:
        ordering = ['-created_at']
        verbose_name = "User Passkey"
        verbose_name_plural = "User Passkeys"
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['credential_id']),
        ]
