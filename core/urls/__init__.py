from django.contrib.admin import site
from django.urls import URLPattern, URLResolver, path

from core.urls.acronym import urlpatterns_acronym
from core.urls.application import urlpatterns_application
from core.urls.application_group import urlpatterns_application_group
from core.urls.database import urlpatterns_database
from core.urls.dependency import urlpatterns_dependency
from core.urls.document import urlpatterns_document
from core.urls.person import urlpatterns_person
from core.urls.release import urlpatterns_release
from core.urls.release_bundle import urlpatterns_release_bundle
from core.views import home_view

urlpatterns: list[URLPattern | URLResolver] = [
    # HOME (INDEX)
    path(name="index", route="", view=home_view),
    path(name="home", route="home", view=home_view),

    # ADMIN
    path(name="admin", route="admin", view=site.urls),

    *urlpatterns_acronym,
    *urlpatterns_application,
    *urlpatterns_application_group,
    *urlpatterns_database,
    *urlpatterns_dependency,
    *urlpatterns_document,
    *urlpatterns_person,
    *urlpatterns_release,
    *urlpatterns_release_bundle,
]
