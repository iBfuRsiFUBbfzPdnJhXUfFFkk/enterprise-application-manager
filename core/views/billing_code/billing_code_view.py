from django.core.paginator import Paginator
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse

from core.models.billing_code import BillingCode
from core.utilities.base_render import base_render


def billing_code_view(request: HttpRequest) -> HttpResponse:
    # Get filter and search parameters
    show_inactive = request.GET.get('show_inactive', 'false').lower() == 'true'
    search_query = request.GET.get('search', '').strip()
    page_number = request.GET.get('page', 1)

    # Start with base queryset
    if show_inactive:
        queryset: QuerySet = BillingCode.objects.all()
    else:
        queryset: QuerySet = BillingCode.objects.filter(is_active=True)

    # Apply search filter if provided
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(billing_code__icontains=search_query) |
            Q(comment__icontains=search_query)
        )

    # Order by active status and name
    queryset = queryset.order_by('-is_active', 'name')

    # Paginate results (25 per page)
    paginator = Paginator(queryset, 25)
    page_obj = paginator.get_page(page_number)

    context = {
        'models': page_obj,
        'page_obj': page_obj,
        'show_inactive': show_inactive,
        'search_query': search_query,
    }

    return base_render(
        context=context,
        request=request,
        template_name='authenticated/billing_code/billing_code.html'
    )
