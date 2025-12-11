from django.urls import URLPattern, URLResolver

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.it_devops_request.it_devops_request_add_view import it_devops_request_add_view
from core.views.it_devops_request.it_devops_request_edit_view import it_devops_request_edit_view
from core.views.it_devops_request.it_devops_request_view import it_devops_request_view


urlpatterns_it_devops_request: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name="it_devops_request",
    view=it_devops_request_view,
    view_edit=it_devops_request_edit_view,
    view_new=it_devops_request_add_view,
)

# Additional patterns will be added later for detail view, DOCX export, and AJAX update
