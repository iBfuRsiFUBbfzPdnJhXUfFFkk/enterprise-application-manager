from django.core.paginator import Paginator
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse

from core.models.application import Application
from core.models.billing_code import BillingCode
from core.models.person import Person
from core.utilities.base_render import base_render


def billing_code_view(request: HttpRequest) -> HttpResponse:
    # Get filter and search parameters
    show_inactive = request.GET.get('show_inactive', 'false').lower() == 'true'
    search_query = request.GET.get('search', '').strip()
    page_number = request.GET.get('page', 1)
    sort_by = request.GET.get('sort', 'name')
    sort_dir = request.GET.get('dir', 'asc')
    application_filter = request.GET.get('application', '')
    project_manager_filter = request.GET.get('project_manager', '')

    # Start with base queryset
    if show_inactive:
        queryset: QuerySet = BillingCode.objects.all()
    else:
        queryset: QuerySet = BillingCode.objects.filter(is_active=True)

    # Apply application filter if provided
    if application_filter:
        queryset = queryset.filter(application_id=application_filter)

    # Apply project manager filter if provided
    if project_manager_filter:
        queryset = queryset.filter(project_manager_id=project_manager_filter)

    # Apply search filter if provided
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(billing_code__icontains=search_query) |
            Q(comment__icontains=search_query)
        )

    # Map sort fields to database fields
    sort_fields = {
        'status': 'is_active',
        'name': 'name',
        'code': 'billing_code',
        'application': 'application__name',
        'group': 'application_group__name',
        'projects': 'projects__name',
    }

    # Get the database field for sorting
    sort_field = sort_fields.get(sort_by, 'name')

    # Apply sorting
    if sort_dir == 'desc':
        sort_field = f'-{sort_field}'

    # For status, reverse the order (active first when asc)
    if sort_by == 'status':
        sort_field = f'-{sort_field}' if sort_dir == 'asc' else sort_field.replace('-', '')

    # For projects, use distinct to avoid duplicates from M2M join
    if sort_by == 'projects':
        queryset = queryset.order_by(sort_field, 'name').distinct()
    else:
        queryset = queryset.order_by(sort_field, 'name')

    # Paginate results (25 per page)
    paginator = Paginator(queryset, 25)
    page_obj = paginator.get_page(page_number)

    # Get applications that have billing codes
    applications_with_billing_codes = Application.objects.filter(
        billingcode__isnull=False
    ).distinct().order_by('name')

    # Get project managers that have billing codes
    project_managers_with_billing_codes = Person.objects.filter(
        billing_codes_managed__isnull=False
    ).distinct().order_by('name_last', 'name_first')

    context = {
        'models': page_obj,
        'page_obj': page_obj,
        'show_inactive': show_inactive,
        'search_query': search_query,
        'sort_by': sort_by,
        'sort_dir': sort_dir,
        'application_filter': application_filter,
        'project_manager_filter': project_manager_filter,
        'applications_with_billing_codes': applications_with_billing_codes,
        'project_managers_with_billing_codes': project_managers_with_billing_codes,
    }

    return base_render(
        context=context,
        request=request,
        template_name='authenticated/billing_code/billing_code.html'
    )
