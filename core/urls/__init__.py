from django.contrib.admin import site
from django.urls import URLPattern, URLResolver, path

from core.urls.application import urlpatterns_application
from core.urls.database import urlpatterns_database
from core.urls.person import urlpatterns_person
from core.views import home_view

urlpatterns: list[URLPattern | URLResolver] = [
    # HOME (INDEX)
    path(name="index", route="", view=home_view),
    path(name="home", route="home", view=home_view),

    # ADMIN
    path(name="admin", route="admin", view=site.urls),

    *urlpatterns_application,
    *urlpatterns_database,
    *urlpatterns_person,
]
