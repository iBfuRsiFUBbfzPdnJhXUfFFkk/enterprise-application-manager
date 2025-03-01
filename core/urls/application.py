from django.urls import URLPattern, URLResolver, path

from core.views.application.application_add_view import application_add_view
from core.views.application.application_edit_view import application_edit_view
from core.views.application.application_view import application_view

urlpatterns_application: list[URLPattern | URLResolver] = [
    path(name="application", route="application/", view=application_view),
    path(name="application_new", route="application/new/", view=application_add_view),
    path(name="application_edit", route="application/edit/<int:model_id>/", view=application_edit_view),
]
