from django.db import models
from core.models.common.abstract.abstract_base_model import AbstractBaseModel


class DatabaseSizeHistory(AbstractBaseModel):
    """Tracks historical database table sizes for trend analysis."""

    _disable_history = True  # Already a history tracking model, meta-history not needed

    table_name = models.CharField(max_length=255, null=True, blank=True)
    size_bytes = models.BigIntegerField(help_text="Size of table data in bytes")
    index_size_bytes = models.BigIntegerField(
        help_text="Size of table indexes in bytes",
        default=0
    )
    row_count = models.IntegerField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True, help_text="When this snapshot was recorded")

    def __str__(self):
        return f"{self.table_name} - {self.size_bytes} bytes ({self.recorded_at})"

    class Meta:
        ordering = ['-recorded_at', 'table_name']
        verbose_name = "Database Size History"
        verbose_name_plural = "Database Size Histories"
        indexes = [
            models.Index(fields=['table_name', '-recorded_at']),
        ]
