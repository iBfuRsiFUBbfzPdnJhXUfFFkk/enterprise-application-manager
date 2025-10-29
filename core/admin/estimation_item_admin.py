from django.contrib import admin
from core.admin.base_model_admin import BaseModelAdmin
from core.models.estimation_item import EstimationItem


@admin.register(EstimationItem)
class EstimationItemAdmin(BaseModelAdmin):
    """Custom admin for EstimationItem to include group field in list display."""

    list_display = ('id', 'title', 'group', 'estimation', 'order', 'story_points', 'complexity_level', 'priority')
    list_filter = ('group', 'estimation', 'complexity_level', 'priority', 'cone_of_uncertainty')
    search_fields = ('title', 'description', 'group')
    list_editable = ('order', 'group')
    ordering = ('estimation', 'order', 'id')
