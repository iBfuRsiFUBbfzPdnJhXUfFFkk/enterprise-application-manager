from django.contrib.admin import site
from django.contrib.auth.decorators import login_required
from django.urls import URLPattern, URLResolver, path, include

from core.urls.urlpatterns_acronym import urlpatterns_acronym
from core.urls.urlpatterns_action import urlpatterns_action
from core.urls.urlpatterns_api import urlpatterns_api
from core.urls.urlpatterns_application import urlpatterns_application
from core.urls.urlpatterns_application_group import urlpatterns_application_group
from core.urls.urlpatterns_billing_code import urlpatterns_billing_code
from core.urls.urlpatterns_client import urlpatterns_client
from core.urls.urlpatterns_command import urlpatterns_command
from core.urls.urlpatterns_cron_job import urlpatterns_cron_job
from core.urls.urlpatterns_data_point import urlpatterns_data_point
from core.urls.urlpatterns_data_use_exception import urlpatterns_data_use_exception
from core.urls.urlpatterns_database import urlpatterns_database
from core.urls.urlpatterns_dependency import urlpatterns_dependency
from core.urls.urlpatterns_document import urlpatterns_document
from core.urls.urlpatterns_external_blocker import urlpatterns_external_blocker
from core.urls.urlpatterns_formula import urlpatterns_formula
from core.urls.urlpatterns_hotfix import urlpatterns_hotfix
from core.urls.urlpatterns_login import urlpatterns_login
from core.urls.urlpatterns_logout import urlpatterns_logout
from core.urls.urlpatterns_person import urlpatterns_person
from core.urls.urlpatterns_profile import urlpatterns_profile
from core.urls.urlpatterns_release import urlpatterns_release
from core.urls.urlpatterns_release_bundle import urlpatterns_release_bundle
from core.urls.urlpatterns_secret import urlpatterns_secret
from core.urls.urlpatterns_server_configuration import urlpatterns_server_configuration
from core.urls.urlpatterns_settings import urlpatterns_settings
from core.urls.urlpatterns_this_api import urlpatterns_this_api
from core.views import home_view
from kpi.urls import urlpatterns_kpi

urlpatterns_authenticated: list[URLPattern | URLResolver] = [
    # HOME (INDEX)
    path(name="index", route="", view=home_view),
    path(name="home", route="home/", view=home_view),

    # ADMIN
    path(name="admin", route="admin/", view=site.urls),

    path(route='hijack/', view=include(arg='hijack.urls')),

    *urlpatterns_acronym,
    *urlpatterns_action,
    *urlpatterns_application,
    *urlpatterns_application_group,
    *urlpatterns_billing_code,
    *urlpatterns_client,
    *urlpatterns_command,
    *urlpatterns_cron_job,
    *urlpatterns_data_point,
    *urlpatterns_data_use_exception,
    *urlpatterns_database,
    *urlpatterns_dependency,
    *urlpatterns_document,
    *urlpatterns_external_blocker,
    *urlpatterns_formula,
    *urlpatterns_hotfix,
    *urlpatterns_logout,
    *urlpatterns_person,
    *urlpatterns_profile,
    *urlpatterns_release,
    *urlpatterns_release_bundle,
    *urlpatterns_secret,
    *urlpatterns_server_configuration,
    *urlpatterns_settings,
    *urlpatterns_this_api,
    path(name="kpi", route='kpi/', view=include(arg=(urlpatterns_kpi, 'kpi'), namespace="kpi")),
    *urlpatterns_api
]

urlpatterns: list[URLPattern | URLResolver] = [
    path(name="index", route="", view=login_required(function=home_view)),
    *urlpatterns_login,
    path(name="authenticated", route='authenticated/', view=include(arg=urlpatterns_authenticated)),
]
