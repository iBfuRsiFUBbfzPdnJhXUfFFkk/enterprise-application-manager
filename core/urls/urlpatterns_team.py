from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.team import (
    team_add_view,
    team_delete_view,
    team_detail_view,
    team_edit_view,
    team_view,
)

urlpatterns_team: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='team',
    view=team_view,
    view_edit=team_edit_view,
    view_new=team_add_view,
)

# Add detail view
urlpatterns_team.append(
    path(name='team_detail', route='team/<int:model_id>/', view=team_detail_view)
)

# Add delete view
urlpatterns_team.append(
    path(name='team_delete', route='team/delete/<int:model_id>/', view=team_delete_view)
)
