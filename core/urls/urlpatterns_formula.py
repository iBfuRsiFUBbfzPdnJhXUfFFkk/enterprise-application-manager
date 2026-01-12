from django.urls import URLPattern, URLResolver, path

from core.views.formula import (
    formula_add_view,
    formula_delete_view,
    formula_detail_view,
    formula_edit_view,
    formula_view,
)

urlpatterns_formula: list[URLPattern | URLResolver] = [
    path("formula/", formula_view, name="formula"),
    path("formula/edit/<int:model_id>/", formula_edit_view, name="formula_edit"),
    path("formula/new/", formula_add_view, name="formula_new"),
    path("formula/<int:model_id>/", formula_detail_view, name="formula_detail"),
    path("formula/delete/<int:model_id>/", formula_delete_view, name="formula_delete"),
]
