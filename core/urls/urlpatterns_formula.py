from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.formula import (
    formula_add_view,
    formula_delete_view,
    formula_detail_view,
    formula_edit_view,
    formula_view,
)

urlpatterns_formula: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='formula',
    view=formula_view,
    view_edit=formula_edit_view,
    view_new=formula_add_view,
)

# Add detail view
urlpatterns_formula.append(
    path(name='formula_detail', route='formula/<int:model_id>/', view=formula_detail_view)
)

# Add delete view
urlpatterns_formula.append(
    path(name='formula_delete', route='formula/delete/<int:model_id>/', view=formula_delete_view)
)
