from django.contrib import admin

from core.models.application_pin import ApplicationPin


@admin.register(ApplicationPin)
class ApplicationPinAdmin(admin.ModelAdmin):
    list_display = ('user', 'application', 'order', 'created', 'modified')
    list_filter = ('user', 'created', 'modified')
    search_fields = ('user__username', 'application__name', 'application__acronym')
    ordering = ('user', 'order', 'id')
    readonly_fields = ('created', 'modified')

    fieldsets = (
        (None, {
            'fields': ('user', 'application', 'order')
        }),
        ('Timestamps', {
            'fields': ('created', 'modified'),
            'classes': ('collapse',)
        }),
    )
