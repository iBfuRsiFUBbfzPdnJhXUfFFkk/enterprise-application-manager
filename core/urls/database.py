from django.urls import URLPattern, URLResolver, path

from core.views.database.database_add_view import database_add_view
from core.views.database.database_edit_view import database_edit_view
from core.views.database.database_view import database_view

urlpatterns_database: list[URLPattern | URLResolver] = [
    path(name="database", route="database", view=database_view),
    path(name="database_new", route="database/new", view=database_add_view),
    path(name="database_edit", route="database/edit/<int:model_id>", view=database_edit_view),
]
