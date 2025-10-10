from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.billing_code import (
    billing_code_add_view,
    billing_code_delete_view,
    billing_code_detail_view,
    billing_code_edit_view,
    billing_code_view,
)

urlpatterns_billing_code: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='billing_code',
    view=billing_code_view,
    view_edit=billing_code_edit_view,
    view_new=billing_code_add_view,
)

# Add detail view
urlpatterns_billing_code.append(
    path(name='billing_code_detail', route='billing_code/<int:model_id>/', view=billing_code_detail_view)
)

# Add delete view
urlpatterns_billing_code.append(
    path(name='billing_code_delete', route='billing_code/delete/<int:model_id>/', view=billing_code_delete_view)
)
