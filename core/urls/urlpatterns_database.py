from django.urls import URLPattern, URLResolver

from core.urls.common.create_generic_urlpatterns import create_generic_urlpatterns
from core.views.database.database_add_view import database_add_view
from core.views.database.database_edit_view import database_edit_view
from core.views.database.database_view import database_view

urlpatterns_database: list[URLPattern | URLResolver] = create_generic_urlpatterns(
    name="database",
    view=database_view,
    view_edit=database_edit_view,
    view_new=database_add_view,
)
