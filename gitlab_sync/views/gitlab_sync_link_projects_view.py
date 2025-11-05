from django.http import HttpRequest, HttpResponse

from core.models.application import Application
from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncProject


def gitlab_sync_link_projects_view(request: HttpRequest) -> HttpResponse:
    """
    Drag-and-drop interface to link GitLab projects to Application records.

    Shows unlinked GitLab projects and Applications, plus existing links.
    """
    unlinked_gitlab_projects = GitLabSyncProject.objects.filter(
        application__isnull=True
    ).order_by("path_with_namespace")

    # Only get linked projects where the application still exists (not deleted)
    linked_gitlab_projects = (
        GitLabSyncProject.objects.filter(application__isnull=False)
        .select_related("application")
        .exclude(application=None)
    )

    applications = Application.objects.all().order_by("name")

    context = {
        "unlinked_gitlab_projects": unlinked_gitlab_projects,
        "linked_gitlab_projects": linked_gitlab_projects,
        "applications": applications,
    }

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/link_projects.html",
        context=context,
    )
