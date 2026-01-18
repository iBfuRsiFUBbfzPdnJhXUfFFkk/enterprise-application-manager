from django.urls import URLPattern, URLResolver, path

from core.views.comment import comment_create_ajax_view, comment_delete_ajax_view

urlpatterns_comment: list[URLPattern | URLResolver] = [
    path(
        name="comment_create_ajax",
        route="comment/create/ajax/",
        view=comment_create_ajax_view,
    ),
    path(
        name="comment_delete_ajax",
        route="comment/<int:comment_id>/delete/ajax/",
        view=comment_delete_ajax_view,
    ),
]
