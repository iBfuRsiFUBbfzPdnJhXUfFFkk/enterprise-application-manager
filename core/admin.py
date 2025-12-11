from django.contrib import admin

from core.models.application_pin import ApplicationPin
from core.models.it_devops_request import ITDevOpsRequest
from core.models.it_devops_request_update import ITDevOpsRequestUpdate


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


@admin.register(ITDevOpsRequest)
class ITDevOpsRequestAdmin(admin.ModelAdmin):
    list_display = ('document_id', 'name', 'status', 'priority', 'person_requester', 'date_requested', 'date_due')
    list_filter = ('status', 'priority', 'date_requested')
    search_fields = ('document_id', 'name', 'description', 'reference_number')
    ordering = ('-date_requested', '-id')
    readonly_fields = ('document_id', 'created', 'modified')

    fieldsets = (
        ('Document Information', {
            'fields': ('document_id', 'name')
        }),
        ('Basic Information', {
            'fields': ('status', 'priority', 'reference_number')
        }),
        ('People', {
            'fields': ('person_requester', 'person_assignee', 'person_approver')
        }),
        ('Related Entities', {
            'fields': ('application', 'project')
        }),
        ('Details', {
            'fields': ('description', 'justification', 'expected_outcome')
        }),
        ('Timeline', {
            'fields': ('date_requested', 'date_due', 'date_completed')
        }),
        ('Attachments', {
            'fields': ('attachments',)
        }),
        ('Additional', {
            'fields': ('comment',)
        }),
        ('Timestamps', {
            'fields': ('created', 'modified'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ITDevOpsRequestUpdate)
class ITDevOpsRequestUpdateAdmin(admin.ModelAdmin):
    list_display = ('it_devops_request', 'person_author', 'datetime_created', 'is_internal_note')
    list_filter = ('is_internal_note', 'datetime_created')
    search_fields = ('it_devops_request__document_id', 'it_devops_request__name', 'comment')
    ordering = ('-datetime_created', '-id')
    readonly_fields = ('datetime_created', 'created', 'modified')

    fieldsets = (
        (None, {
            'fields': ('it_devops_request', 'person_author', 'comment', 'is_internal_note')
        }),
        ('Timestamps', {
            'fields': ('datetime_created', 'created', 'modified'),
            'classes': ('collapse',)
        }),
    )
