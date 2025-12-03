from datetime import datetime, timezone
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from docx import Document

from core.models.application import Application
from core.views.application.utilities.application_docx_helpers import (
    add_application_heading,
    add_header_footer,
    add_title_page,
    add_toc_placeholder,
    set_narrow_margins,
)
from core.views.application.utilities.application_docx_sections import (
    add_basic_info_section,
    add_compliance_section,
    add_links_section,
    add_team_section,
    add_technical_config_section,
)
from core.views.application.utilities.application_docx_sections_extra import (
    add_description_section,
    add_groups_and_dependencies_section,
    add_procedures_section,
    add_tools_and_services_section,
)
from core.views.generic.generic_500 import generic_500


@login_required
def application_export_docx_view(request: HttpRequest) -> HttpResponse:
    """Export applications to DOCX document with filter support."""
    try:
        # Get filter parameters from query string
        search_term = request.GET.get('search', '').lower()
        platform_filter = request.GET.get('platform', '').lower()
        legacy_filter = request.GET.get('legacy', '')
        pipeline_filter = request.GET.get('pipeline', '').lower()

        # Query applications with optimized prefetch
        applications = Application.objects.all().select_related(
            'application_group_platform',
            'person_product_owner',
            'person_product_manager',
            'person_project_manager',
            'person_scrum_master',
            'person_architect',
            'person_lead_developer',
        ).prefetch_related(
            'person_developers',
            'person_smes',
            'person_stakeholders',
            'application_groups',
            'tools',
            'service_providers',
            'application_upstream_dependencies',
            'application_downstream_dependencies',
            'procedure_steps',
        ).order_by('name', 'acronym')

        # Apply filters
        if search_term:
            applications = applications.filter(
                Q(name__icontains=search_term)
                | Q(acronym__icontains=search_term)
                | Q(type_platform_target__icontains=search_term)
            )
        if platform_filter:
            applications = applications.filter(type_platform_target__iexact=platform_filter)
        if legacy_filter == 'legacy':
            applications = applications.filter(is_legacy=True)
        elif legacy_filter == 'active':
            applications = applications.filter(is_legacy=False)
        if pipeline_filter:
            applications = applications.filter(pipeline_status__iexact=pipeline_filter)

        # Create document
        document = Document()
        set_narrow_margins(document)
        add_header_footer(document, 'Enterprise Applications Export')

        # Add title page
        username = request.user.get_full_name() or request.user.username
        add_title_page(document, username, applications.count())

        # Add TOC placeholder
        add_toc_placeholder(document)

        # Add each application
        for i, application in enumerate(applications):
            # Application heading (H1 for TOC)
            add_application_heading(document, application)

            # Add sections
            add_basic_info_section(document, application)
            add_technical_config_section(document, application)
            add_compliance_section(document, application)
            add_team_section(document, application)
            add_links_section(document, application)
            add_groups_and_dependencies_section(document, application)
            add_tools_and_services_section(document, application)
            add_description_section(document, application)
            add_procedures_section(document, application)

            # Add page break (except for last application)
            if i < applications.count() - 1:
                document.add_page_break()

        # Generate filename
        now = datetime.now(timezone.utc)
        timestamp = now.strftime('%Y-%m-%d__%I:%M:%p').lower().replace(' ', '')
        filename = f'applications_export__{timestamp}.docx'

        # Save to BytesIO
        file_stream = BytesIO()
        document.save(file_stream)
        file_stream.seek(0)

        # Return as HTTP response
        response = HttpResponse(
            file_stream.read(),
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response

    except Exception:
        return generic_500(request=request)
