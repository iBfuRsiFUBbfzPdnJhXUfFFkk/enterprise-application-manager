from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from core.models.application_pin import ApplicationPin
from core.models.comment import Comment
from core.models.competitor import Competitor
from core.models.it_devops_request import ITDevOpsRequest
from core.models.it_devops_request_update import ITDevOpsRequestUpdate
from core.models.maintenance_window import MaintenanceWindow
from core.models.meeting import Meeting
from core.models.meeting_action_item import MeetingActionItem
from core.models.meeting_note import MeetingNote


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


@admin.register(Competitor)
class CompetitorAdmin(admin.ModelAdmin):
    list_display = ('name', 'acronym', 'market_segment', 'employee_count_tier', 'revenue_tier')
    list_filter = ('employee_count_tier', 'revenue_tier', 'market_segment')
    search_fields = ('name', 'acronym', 'primary_products', 'market_segment', 'location_city', 'location_state_code')
    ordering = ('name', '-id')
    readonly_fields = ('created', 'modified')
    filter_horizontal = ('competing_applications', 'organizations')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'acronym', 'url')
        }),
        ('Location', {
            'fields': ('location_address', 'location_address_continued', 'location_city',
                      'location_county', 'location_state_code', 'location_postal_code',
                      'location_latitude', 'location_longitude'),
            'classes': ('collapse',)
        }),
        ('Business Intelligence', {
            'fields': ('primary_products', 'market_segment', 'employee_count_tier',
                      'revenue_tier', 'year_founded')
        }),
        ('Relationships', {
            'fields': ('competing_applications', 'organizations')
        }),
        ('Additional Information', {
            'fields': ('comment',)
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


@admin.register(MaintenanceWindow)
class MaintenanceWindowAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_time_start', 'date_time_end', 'severity', 'status', 'person_contact')
    list_filter = ('severity', 'status', 'date_time_start')
    search_fields = ('name', 'description', 'person_contact__full_name')
    ordering = ('-date_time_start', '-id')
    readonly_fields = ('created', 'modified')
    filter_horizontal = ('applications_affected',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'comment')
        }),
        ('Schedule', {
            'fields': ('date_time_start', 'date_time_end', 'severity', 'status')
        }),
        ('Related Information', {
            'fields': ('person_contact', 'person_created_by', 'applications_affected')
        }),
        ('Timestamps', {
            'fields': ('created', 'modified'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('name', 'meeting_type', 'status', 'organizer', 'datetime_start', 'duration_hours')
    list_filter = ('status', 'meeting_type', 'datetime_start')
    search_fields = ('name', 'description', 'agenda', 'organizer__name_first', 'organizer__name_last')
    ordering = ('-datetime_start', '-id')
    readonly_fields = ('duration_hours', 'is_in_progress', 'created', 'modified')
    filter_horizontal = ('attendees',)

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'meeting_type', 'status', 'organizer')
        }),
        ('Schedule', {
            'fields': ('datetime_start', 'datetime_end', 'duration_hours', 'is_in_progress')
        }),
        ('Attendees', {
            'fields': ('attendees',)
        }),
        ('Location', {
            'fields': ('location_address', 'location_address_continued', 'location_city',
                      'location_county', 'location_state_code', 'location_postal_code',
                      'virtual_meeting_url'),
            'classes': ('collapse',)
        }),
        ('Content', {
            'fields': ('description', 'agenda', 'minutes')
        }),
        ('Related Entities', {
            'fields': ('application', 'project')
        }),
        ('Additional Information', {
            'fields': ('comment',)
        }),
        ('Timestamps', {
            'fields': ('created', 'modified'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MeetingActionItem)
class MeetingActionItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'meeting', 'assignee', 'status', 'priority', 'due_date')
    list_filter = ('status', 'priority', 'due_date')
    search_fields = ('name', 'description', 'meeting__name', 'assignee__name_first', 'assignee__name_last')
    ordering = ('status', '-priority', 'due_date', '-id')
    readonly_fields = ('created', 'modified')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'meeting', 'assignee')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'due_date', 'date_completed')
        }),
        ('Details', {
            'fields': ('description', 'comment')
        }),
        ('Timestamps', {
            'fields': ('created', 'modified'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MeetingNote)
class MeetingNoteAdmin(admin.ModelAdmin):
    list_display = ('meeting', 'note_type', 'person', 'datetime_created', 'content_preview')
    list_filter = ('note_type', 'datetime_created')
    search_fields = ('content', 'meeting__name', 'person__name_first', 'person__name_last')
    ordering = ('-datetime_created', '-id')
    readonly_fields = ('datetime_created', 'created', 'modified')

    fieldsets = (
        ('Basic Information', {
            'fields': ('meeting', 'note_type', 'person')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Timestamps', {
            'fields': ('datetime_created', 'created', 'modified'),
            'classes': ('collapse',)
        }),
    )

    def content_preview(self, obj):
        return obj.content[:75] + '...' if len(obj.content) > 75 else obj.content

    content_preview.short_description = 'Content Preview'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_type', 'object_id', 'created_by', 'is_internal', 'created_at', 'content_preview')
    list_filter = ('is_internal', 'content_type', 'created_at')
    search_fields = ('content', 'created_by__username')
    ordering = ('-created_at', '-id')
    readonly_fields = ('created_at', 'modified_at', 'created', 'modified')
    raw_id_fields = ('created_by',)

    fieldsets = (
        ('Target Object', {
            'fields': ('content_type', 'object_id')
        }),
        ('Comment', {
            'fields': ('content', 'is_internal', 'created_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'modified_at', 'created', 'modified'),
            'classes': ('collapse',)
        }),
    )

    def content_preview(self, obj):
        return obj.content[:75] + '...' if len(obj.content) > 75 else obj.content

    content_preview.short_description = 'Content Preview'
