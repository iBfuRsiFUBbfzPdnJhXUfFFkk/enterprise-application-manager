from django.urls import URLPattern, URLResolver, path

from core.views.this_api.this_api_create_sprint_kpis_view import this_api_create_sprint_kpis_view
from core.views.this_api.this_api_sync_gitlab_users_view import this_api_sync_gitlab_users_view
from core.views.this_api.this_api_update_code_churn_view.this_api_update_code_churn_view import \
    this_api_update_code_churn_view
from core.views.this_api.this_api_update_code_reviews.this_api_update_code_reviews_view import \
    this_api_update_code_reviews_view
from core.views.this_api.this_api_update_issues_authored_view.this_api_update_issues_authored_view import \
    this_api_update_issues_authored_view
from core.views.this_api.this_api_update_sprint_committed_issues_view.this_api_update_sprint_committed_issues_view import \
    this_api_update_sprint_committed_issues_view
from core.views.this_api.this_api_update_sprint_delivered_issues_view.this_api_update_sprint_delivered_issues_view import \
    this_api_update_sprint_delivered_issues_view

urlpatterns_this_api: list[URLPattern | URLResolver] = [
    path(name="this_api_update_sprint_delivered_issues", route="api/update_sprint_delivered_issues/", view=this_api_update_sprint_delivered_issues_view),
    path(name="this_api_create_sprint_kpis", route="api/create_sprint_kpis/", view=this_api_create_sprint_kpis_view),
    path(name="this_api_sync_gitlab_users", route="api/sync_gitlab_users/", view=this_api_sync_gitlab_users_view),
    path(name="this_api_update_code_churn", route="api/update_code_churn/", view=this_api_update_code_churn_view),
    path(name="this_api_update_code_reviews", route="api/update_code_reviews/", view=this_api_update_code_reviews_view),
    path(name="this_api_update_sprint_committed_issues", route="api/update_sprint_committed_issues/", view=this_api_update_sprint_committed_issues_view),
    path(name="this_api_update_issues_authored", route="api/update_issues_authored/",
         view=this_api_update_issues_authored_view),
]
