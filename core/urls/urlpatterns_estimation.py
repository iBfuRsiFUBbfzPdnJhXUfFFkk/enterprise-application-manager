from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.estimation.estimation_add_view import estimation_add_view
from core.views.estimation.estimation_delete_view import estimation_delete_view
from core.views.estimation.estimation_detail_view import estimation_detail_view
from core.views.estimation.estimation_edit_view import estimation_edit_view
from core.views.estimation.estimation_export_docx_view import estimation_export_docx_view
from core.views.estimation.estimation_item_add_view import estimation_item_add_view
from core.views.estimation.estimation_item_delete_view import estimation_item_delete_view
from core.views.estimation.estimation_item_edit_view import estimation_item_edit_view
from core.views.estimation.estimation_item_move_up_view import estimation_item_move_up_view
from core.views.estimation.estimation_item_move_down_view import estimation_item_move_down_view
from core.views.estimation.estimation_view import estimation_view

urlpatterns_estimation: list[URLPattern | URLResolver] = [
    *create_generic_urlpatterns(
        name="estimation",
        view=estimation_view,
        view_edit=estimation_edit_view,
        view_new=estimation_add_view,
    ),
    path(name="estimation_detail", route="estimation/<int:model_id>/", view=estimation_detail_view),
    path(name="estimation_delete", route="estimation/delete/<int:model_id>/", view=estimation_delete_view),
    path(name="estimation_export_docx", route="estimation/<int:model_id>/export/", view=estimation_export_docx_view),

    # Estimation item URLs
    path(name="estimation_item_add", route="estimation/<int:estimation_id>/item/add/", view=estimation_item_add_view),
    path(name="estimation_item_edit", route="estimation/item/<int:item_id>/edit/", view=estimation_item_edit_view),
    path(name="estimation_item_delete", route="estimation/item/<int:item_id>/delete/", view=estimation_item_delete_view),
    path(name="estimation_item_move_up", route="estimation/item/<int:item_id>/move-up/", view=estimation_item_move_up_view),
    path(name="estimation_item_move_down", route="estimation/item/<int:item_id>/move-down/", view=estimation_item_move_down_view),
]
