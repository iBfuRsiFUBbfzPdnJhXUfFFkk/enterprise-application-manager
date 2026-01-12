from django.urls import URLPattern, URLResolver, path

from core.views.policy import (
    policy_add_view,
    policy_delete_view,
    policy_detail_view,
    policy_edit_view,
    policy_view,
)

urlpatterns_policy: list[URLPattern | URLResolver] = [
    path("policy/", policy_view, name="policy"),
    path("policy/edit/<int:model_id>/", policy_edit_view, name="policy_edit"),
    path("policy/new/", policy_add_view, name="policy_new"),
    path("policy/<int:model_id>/", policy_detail_view, name="policy_detail"),
    path("policy/delete/<int:model_id>/", policy_delete_view, name="policy_delete"),
]
