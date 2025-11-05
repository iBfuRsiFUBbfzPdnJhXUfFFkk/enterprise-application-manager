from django.http import HttpRequest, HttpResponse

from core.models.person import Person
from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncUser


def gitlab_sync_link_users_view(request: HttpRequest) -> HttpResponse:
    """
    Drag-and-drop interface to link GitLab users to Person records.

    Shows unlinked GitLab users and People, plus existing links.
    """
    unlinked_gitlab_users = GitLabSyncUser.objects.filter(person__isnull=True).order_by(
        "username"
    )
    # Only get linked users where the person still exists (not deleted)
    linked_gitlab_users = GitLabSyncUser.objects.filter(
        person__isnull=False
    ).select_related("person").exclude(person=None)
    people = Person.objects.filter(is_active=True).order_by("name_last", "name_first")

    context = {
        "unlinked_gitlab_users": unlinked_gitlab_users,
        "linked_gitlab_users": linked_gitlab_users,
        "people": people,
    }

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/link_users.html",
        context=context,
    )
