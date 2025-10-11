from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.policy import (
    policy_add_view,
    policy_delete_view,
    policy_detail_view,
    policy_edit_view,
    policy_view,
)

urlpatterns_policy: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name='policy',
    view=policy_view,
    view_edit=policy_edit_view,
    view_new=policy_add_view,
)

# Add detail view
urlpatterns_policy.append(
    path(name='policy_detail', route='policy/<int:model_id>/', view=policy_detail_view)
)

# Add delete view
urlpatterns_policy.append(
    path(name='policy_delete', route='policy/delete/<int:model_id>/', view=policy_delete_view)
)
