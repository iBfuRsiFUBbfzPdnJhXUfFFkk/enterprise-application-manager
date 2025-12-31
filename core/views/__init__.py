from django.http import HttpRequest, HttpResponse

from core.models.acronym import Acronym
from core.models.action import Action
from core.models.application import Application
from core.models.application_group import ApplicationGroup
from core.models.database import Database
from core.models.dependency import Dependency
from core.models.document import Document
from core.models.person import Person
from core.models.release import Release
from core.models.release_bundle import ReleaseBundle
from core.models.secret import Secret
from core.models.task import Task
from core.utilities.base_render import base_render


def home_view(request: HttpRequest) -> HttpResponse:
    """
    Home page view with database statistics dashboard.
    """
    # Gather statistics from main models
    stats = {
        'applications': Application.objects.count(),
        'application_groups': ApplicationGroup.objects.count(),
        'people': Person.objects.count(),
        'databases': Database.objects.count(),
        'dependencies': Dependency.objects.count(),
        'documents': Document.objects.count(),
        'releases': Release.objects.count(),
        'release_bundles': ReleaseBundle.objects.count(),
        'acronyms': Acronym.objects.count(),
        'actions': Action.objects.count(),
        'secrets': Secret.objects.count() if request.user.is_superuser else 0,
    }

    # Calculate total records
    stats['total_records'] = sum(stats.values())

    # Get the 10 most recent tasks
    tasks = Task.objects.all()[:10]

    context = {
        'stats': stats,
        'tasks': tasks,
    }

    return base_render(
        request=request,
        template_name="authenticated/home/home.html",
        context=context
    )
