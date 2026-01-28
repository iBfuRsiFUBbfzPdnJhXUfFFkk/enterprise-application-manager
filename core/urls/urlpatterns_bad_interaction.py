from django.urls import URLPattern, URLResolver, path

from core.views.bad_interaction import (
    bad_interaction_add_update_view,
    bad_interaction_add_view,
    bad_interaction_delete_view,
    bad_interaction_detail_view,
    bad_interaction_edit_view,
    bad_interaction_fix_evidence_view,
    bad_interaction_list_evidence_files_view,
    bad_interaction_view,
)

urlpatterns_bad_interaction: list[URLPattern | URLResolver] = [
    path("bad_interaction/", bad_interaction_view, name="bad_interaction"),
    path("bad_interaction/edit/<int:model_id>/", bad_interaction_edit_view, name="bad_interaction_edit"),
    path("bad_interaction/new/", bad_interaction_add_view, name="bad_interaction_new"),
    path("bad-interaction/<int:model_id>/", bad_interaction_detail_view, name="bad_interaction_detail"),
    path("bad-interaction/delete/<int:model_id>/", bad_interaction_delete_view, name="bad_interaction_delete"),
    path("bad-interaction/<int:model_id>/add-update/", bad_interaction_add_update_view, name="bad_interaction_add_update"),
    path("bad-interaction/<int:model_id>/fix-evidence/", bad_interaction_fix_evidence_view, name="bad_interaction_fix_evidence"),
    path("bad-interaction/evidence-files/", bad_interaction_list_evidence_files_view, name="bad_interaction_list_evidence_files"),
]
