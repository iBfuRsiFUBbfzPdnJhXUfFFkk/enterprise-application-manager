from django.urls import URLPattern, URLResolver, path

from core.views.database.database_add_view import database_add_view
from core.views.database.database_detail_view import database_detail_view
from core.views.database.database_edit_view import database_edit_view
from core.views.database.database_view import database_view

urlpatterns_database: list[URLPattern | URLResolver] = [
    path("database/", database_view, name="database"),
    path("database/detail/<int:model_id>/", database_detail_view, name="database_detail"),
    path("database/edit/<int:model_id>/", database_edit_view, name="database_edit"),
    path("database/new/", database_add_view, name="database_new"),
]
