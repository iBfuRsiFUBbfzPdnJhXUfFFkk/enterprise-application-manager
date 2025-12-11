from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.it_devops_request.it_devops_request_add_view import it_devops_request_add_view
from core.views.it_devops_request.it_devops_request_detail_view import it_devops_request_detail_view
from core.views.it_devops_request.it_devops_request_edit_view import it_devops_request_edit_view
from core.views.it_devops_request.it_devops_request_export_docx_view import it_devops_request_export_docx_view
from core.views.it_devops_request.it_devops_request_update_add_ajax_view import it_devops_request_update_add_ajax_view
from core.views.it_devops_request.it_devops_request_view import it_devops_request_view


urlpatterns_it_devops_request: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name="it_devops_request",
    view=it_devops_request_view,
    view_edit=it_devops_request_edit_view,
    view_new=it_devops_request_add_view,
)

urlpatterns_it_devops_request.extend(
    [
        path(
            route="it-devops-request/<int:model_id>/detail/",
            view=it_devops_request_detail_view,
            name="it_devops_request_detail",
        ),
        path(
            route="it-devops-request/export/docx/",
            view=it_devops_request_export_docx_view,
            name="it_devops_request_export_docx",
        ),
        path(
            route="it-devops-request/<int:model_id>/update/add/",
            view=it_devops_request_update_add_ajax_view,
            name="it_devops_request_update_add",
        ),
    ]
)
