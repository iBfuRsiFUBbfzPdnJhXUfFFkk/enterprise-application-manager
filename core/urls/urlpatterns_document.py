from django.urls import URLPattern, URLResolver, path

from core.views.document.document_add_view import document_add_view
from core.views.document.document_create_ajax_view import document_create_ajax_view
from core.views.document.document_delete_view import document_delete_view
from core.views.document.document_detail_view import document_detail_view
from core.views.document.document_duplicates_view import document_duplicates_view
from core.views.document.document_edit_view import document_edit_view
from core.views.document.document_file_view import document_file_view
from core.views.document.document_merge_duplicates_view import document_merge_duplicates_view
from core.views.document.document_rehash_view import document_rehash_view
from core.views.document.document_rename_files_view import document_rename_files_view
from core.views.document.document_similar_images_view import document_similar_images_view
from core.views.document.document_view import document_view

urlpatterns_document: list[URLPattern | URLResolver] = [
    path("document/", document_view, name="document"),
    path("document/edit/<int:model_id>/", document_edit_view, name="document_edit"),
    path("document/delete/<int:model_id>/", document_delete_view, name="document_delete"),
    path("document/new/", document_add_view, name="document_new"),
    path("document/detail/<int:model_id>/", document_detail_view, name="document_detail"),
    path("document/create/ajax/", document_create_ajax_view, name="document_create_ajax"),
    path("document/file/<int:model_id>/", document_file_view, name="document_file"),
    path("document/rename-files/", document_rename_files_view, name="document_rename_files"),
    path("document/rehash/", document_rehash_view, name="document_rehash"),
    path("document/duplicates/", document_duplicates_view, name="document_duplicates"),
    path("document/merge-duplicates/", document_merge_duplicates_view, name="document_merge_duplicates"),
    path("document/similar-images/", document_similar_images_view, name="document_similar_images"),
]
