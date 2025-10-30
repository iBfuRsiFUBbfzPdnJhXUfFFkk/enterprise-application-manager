from django.db import models

from core.models.common.abstract.abstract_base_model import AbstractBaseModel
from core.models.common.abstract.abstract_comment import AbstractComment
from core.models.common.abstract.abstract_name import AbstractName
from core.models.common.abstract.abstract_uniform_resource_locator import AbstractUniformResourceLocator
from core.utilities.generate_short_code import generate_unique_short_code


class Link(AbstractBaseModel, AbstractComment, AbstractName, AbstractUniformResourceLocator):
    # Short URL fields
    short_code = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        null=True,
        blank=True,
        help_text='Unique short code for generating short URLs (e.g., "abc123"). Auto-generated if left blank.',
    )

    click_count = models.IntegerField(
        default=0,
        help_text='Number of times this link has been accessed via short URL',
    )

    first_accessed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Timestamp when the link was first accessed via short URL',
    )

    last_accessed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Timestamp when the link was last accessed via short URL',
    )

    is_short_url_active = models.BooleanField(
        default=True,
        help_text='Whether the short URL is active and can be used for redirects',
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['name', '-id']

    def save(self, *args, **kwargs):
        """Generate short code if not provided."""
        if not self.short_code:
            self.short_code = generate_unique_short_code(Link, field_name='short_code', length=10)
        super().save(*args, **kwargs)

    @property
    def get_short_url(self) -> str:
        """
        Get the full short URL path for this link.
        Returns: String like '/-/abc123xyz0'
        """
        if self.short_code:
            return f"/-/{self.short_code}/"
        return ""

    @property
    def get_full_short_url(self) -> str:
        """
        Get the absolute URL for the short link redirect.
        This is used for displaying the full URL to users.
        """
        if self.short_code:
            from django.contrib.sites.models import Site
            try:
                current_site = Site.objects.get_current()
                protocol = 'https' if hasattr(current_site, 'domain') else 'http'
                return f"{protocol}://{current_site.domain}/-/{self.short_code}/"
            except Exception:
                # Fallback if Sites framework is not configured
                return self.get_short_url
        return ""
