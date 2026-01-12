from datetime import timedelta

from django.db import models
from django.utils import timezone

from core.models.common.abstract.abstract_base_model import AbstractBaseModel

CHALLENGE_TYPE_REGISTRATION = 'registration'
CHALLENGE_TYPE_AUTHENTICATION = 'authentication'

CHALLENGE_TYPE_CHOICES = [
    (CHALLENGE_TYPE_REGISTRATION, 'Registration'),
    (CHALLENGE_TYPE_AUTHENTICATION, 'Authentication'),
]


class PasskeyChallenge(AbstractBaseModel):
    """
    Temporary storage for WebAuthn challenges during registration/authentication.
    Challenges expire after 5 minutes for security.
    """

    _disable_history = True  # Temporary data, expires in 5 minutes

    challenge_type: str = models.CharField(max_length=255, choices=CHALLENGE_TYPE_CHOICES, null=True, blank=True)
    challenge: str = models.TextField()
    user = models.ForeignKey(
        to='core.User', on_delete=models.CASCADE, related_name='passkey_challenges', null=True, blank=True
    )
    session_key: str | None = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    used: bool = models.BooleanField(null=True, blank=True, default=False)

    def save(self, *args, **kwargs):
        """Set expiration to 5 minutes from creation if not already set."""
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    def is_valid(self) -> bool:
        """Check if challenge is still valid (not expired and not used)."""
        return not self.used and self.expires_at > timezone.now()

    def __str__(self):
        user_str = self.user.username if self.user else "anonymous"
        return f"{self.challenge_type} - {user_str} - {self.created_at}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Passkey Challenge"
        verbose_name_plural = "Passkey Challenges"
        indexes = [
            models.Index(fields=['challenge', 'challenge_type']),
            models.Index(fields=['session_key']),
            models.Index(fields=['-created_at']),
        ]
