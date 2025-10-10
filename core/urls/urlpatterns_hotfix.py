from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.hotfix import (
    hotfix_add_view,
    hotfix_delete_view,
    hotfix_detail_view,
    hotfix_edit_view,
    hotfix_view,
)

urlpatterns_hotfix: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='hotfix',
    view=hotfix_view,
    view_edit=hotfix_edit_view,
    view_new=hotfix_add_view,
)

# Add detail view
urlpatterns_hotfix.append(
    path(name='hotfix_detail', route='hotfix/<int:model_id>/', view=hotfix_detail_view)
)

# Add delete view
urlpatterns_hotfix.append(
    path(name='hotfix_delete', route='hotfix/delete/<int:model_id>/', view=hotfix_delete_view)
)
