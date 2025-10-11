from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.skill import (
    skill_add_view,
    skill_delete_view,
    skill_detail_view,
    skill_edit_view,
    skill_view,
)

urlpatterns_skill: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='skill',
    view=skill_view,
    view_edit=skill_edit_view,
    view_new=skill_add_view,
)

# Add detail view
urlpatterns_skill.append(
    path(name='skill_detail', route='skill/<int:model_id>/', view=skill_detail_view)
)

# Add delete view
urlpatterns_skill.append(
    path(name='skill_delete', route='skill/delete/<int:model_id>/', view=skill_delete_view)
)
