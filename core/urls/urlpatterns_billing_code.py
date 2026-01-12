from django.urls import URLPattern, URLResolver, path

from core.views.billing_code import (
    billing_code_add_view,
    billing_code_delete_view,
    billing_code_detail_view,
    billing_code_edit_view,
    billing_code_view,
)

urlpatterns_billing_code: list[URLPattern | URLResolver] = [
    path("billing_code/", billing_code_view, name="billing_code"),
    path("billing_code/edit/<int:model_id>/", billing_code_edit_view, name="billing_code_edit"),
    path("billing_code/new/", billing_code_add_view, name="billing_code_new"),
    path("billing_code/<int:model_id>/", billing_code_detail_view, name="billing_code_detail"),
    path("billing_code/delete/<int:model_id>/", billing_code_delete_view, name="billing_code_delete"),
]
