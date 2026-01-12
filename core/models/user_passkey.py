from django.db import models
from django.utils import timezone

from core.models.common.abstract.abstract_base_model import AbstractBaseModel

class UserPasskey(AbstractBaseModel):
    """
    Stores WebAuthn passkey credentials for users.
    Each user can have multiple passkeys (different devices).
    """

    user = models.ForeignKey('core.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='passkeys')
    name: str = models.CharField(max_length=255, null=True, blank=True)
    credential_id: str = models.TextField(unique=True)
    public_key: str = models.TextField()
    sign_count: int = models.IntegerField(default=0)
    aaguid: str | None = models.CharField(max_length=255, null=True, blank=True)
    credential_type: str = models.CharField(max_length=255, null=True, blank=True)
    transports: str | None = models.CharField(max_length=255, null=True, blank=True)
    backup_eligible: bool = models.BooleanField(null=True, blank=True, default=False)
    backup_state: bool = models.BooleanField(null=True, blank=True, default=False)
    user_verified: bool = models.BooleanField(null=True, blank=True, default=False)
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
