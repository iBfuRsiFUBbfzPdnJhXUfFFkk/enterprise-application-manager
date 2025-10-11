from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.term import (
    term_add_view,
    term_delete_view,
    term_detail_view,
    term_edit_view,
    term_view,
)

urlpatterns_term: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='term',
    view=term_view,
    view_edit=term_edit_view,
    view_new=term_add_view,
)

# Add detail view
urlpatterns_term.append(
    path(name='term_detail', route='term/<int:model_id>/', view=term_detail_view)
)

# Add delete view
urlpatterns_term.append(
    path(name='term_delete', route='term/delete/<int:model_id>/', view=term_delete_view)
)
