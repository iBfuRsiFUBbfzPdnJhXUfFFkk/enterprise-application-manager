from django.urls import URLPattern, URLResolver, path

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.estimation.estimation_add_view import estimation_add_view
from core.views.estimation.estimation_delete_view import estimation_delete_view
from core.views.estimation.estimation_detail_view import estimation_detail_view
from core.views.estimation.estimation_edit_view import estimation_edit_view
from core.views.estimation.estimation_export_docx_view import estimation_export_docx_view
from core.views.estimation.estimation_fix_item_order_view import estimation_fix_item_order_view
from core.views.estimation.estimation_group_rename_view import estimation_group_rename_view
from core.views.estimation.estimation_group_move_up_view import estimation_group_move_up_view
from core.views.estimation.estimation_group_move_down_view import estimation_group_move_down_view
from core.views.estimation.estimation_group_move_to_top_view import estimation_group_move_to_top_view
from core.views.estimation.estimation_group_move_to_bottom_view import estimation_group_move_to_bottom_view
from core.views.estimation.estimation_recalculate_all_items_view import estimation_recalculate_all_items_view
from core.views.estimation.estimation_item_add_view import estimation_item_add_view
from core.views.estimation.estimation_item_delete_view import estimation_item_delete_view
from core.views.estimation.estimation_item_detail_view import estimation_item_detail_view
from core.views.estimation.estimation_item_duplicate_view import estimation_item_duplicate_view
from core.views.estimation.estimation_item_edit_view import estimation_item_edit_view
from core.views.estimation.estimation_item_move_down_view import estimation_item_move_down_view
from core.views.estimation.estimation_item_move_to_bottom_view import estimation_item_move_to_bottom_view
from core.views.estimation.estimation_item_move_to_top_view import estimation_item_move_to_top_view
from core.views.estimation.estimation_item_move_up_view import estimation_item_move_up_view
from core.views.estimation.estimation_item_reorder_view import estimation_item_reorder_view
from core.views.estimation.estimation_item_enhance_description_view import estimation_item_enhance_description_view
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
    path(name="estimation_fix_item_order", route="estimation/<int:model_id>/fix-order/", view=estimation_fix_item_order_view),
    path(name="estimation_recalculate_all_items", route="estimation/<int:model_id>/recalculate-all/", view=estimation_recalculate_all_items_view),
    path(name="estimation_group_rename", route="estimation/<int:estimation_id>/group/rename/", view=estimation_group_rename_view),
    path(name="estimation_group_move_up", route="estimation/<int:estimation_id>/group/<str:group_name>/move-up/", view=estimation_group_move_up_view),
    path(name="estimation_group_move_down", route="estimation/<int:estimation_id>/group/<str:group_name>/move-down/", view=estimation_group_move_down_view),
    path(name="estimation_group_move_to_top", route="estimation/<int:estimation_id>/group/<str:group_name>/move-to-top/", view=estimation_group_move_to_top_view),
    path(name="estimation_group_move_to_bottom", route="estimation/<int:estimation_id>/group/<str:group_name>/move-to-bottom/", view=estimation_group_move_to_bottom_view),

    # Estimation item URLs
    path(name="estimation_item_add", route="estimation/<int:estimation_id>/item/add/", view=estimation_item_add_view),
    path(name="estimation_item_detail", route="estimation/item/<int:item_id>/", view=estimation_item_detail_view),
    path(name="estimation_item_edit", route="estimation/item/<int:item_id>/edit/", view=estimation_item_edit_view),
    path(name="estimation_item_delete", route="estimation/item/<int:item_id>/delete/", view=estimation_item_delete_view),
    path(name="estimation_item_duplicate", route="estimation/item/<int:item_id>/duplicate/", view=estimation_item_duplicate_view),
    path(name="estimation_item_move_up", route="estimation/item/<int:item_id>/move-up/", view=estimation_item_move_up_view),
    path(name="estimation_item_move_down", route="estimation/item/<int:item_id>/move-down/", view=estimation_item_move_down_view),
    path(name="estimation_item_move_to_top", route="estimation/item/<int:item_id>/move-to-top/", view=estimation_item_move_to_top_view),
    path(name="estimation_item_move_to_bottom", route="estimation/item/<int:item_id>/move-to-bottom/", view=estimation_item_move_to_bottom_view),
    path(name="estimation_item_reorder", route="estimation/item/reorder/", view=estimation_item_reorder_view),
    path(name="estimation_item_enhance_description", route="estimation/item/enhance-description/", view=estimation_item_enhance_description_view),
]
