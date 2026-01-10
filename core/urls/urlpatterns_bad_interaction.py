from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.bad_interaction import (
    bad_interaction_add_update_view,
    bad_interaction_add_view,
    bad_interaction_delete_view,
    bad_interaction_detail_view,
    bad_interaction_edit_view,
    bad_interaction_view,
)

urlpatterns_bad_interaction: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='bad_interaction',
    view=bad_interaction_view,
    view_edit=bad_interaction_edit_view,
    view_new=bad_interaction_add_view,
)

# Add detail view
urlpatterns_bad_interaction.append(
    path(name='bad_interaction_detail', route='bad-interaction/<int:model_id>/', view=bad_interaction_detail_view)
)

# Add delete view
urlpatterns_bad_interaction.append(
    path(name='bad_interaction_delete', route='bad-interaction/delete/<int:model_id>/', view=bad_interaction_delete_view)
)

# Add update views
urlpatterns_bad_interaction.append(
    path(name='bad_interaction_add_update', route='bad-interaction/<int:model_id>/add-update/', view=bad_interaction_add_update_view)
)
