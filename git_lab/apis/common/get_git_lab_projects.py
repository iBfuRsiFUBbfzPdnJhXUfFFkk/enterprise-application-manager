from django.db.models import Q, QuerySet

from core.settings.common.developer import DEBUG
from core.utilities.cast_query_set import cast_query_set
from git_lab.models.git_lab_project import GitLabProject


def get_git_lab_projects() -> QuerySet[GitLabProject]:
    models: QuerySet[GitLabProject] = cast_query_set(
        typ=GitLabProject,
        val=GitLabProject.objects.filter(~Q(should_skip=True))
    )
    if DEBUG is True:
        print(f"Using Projects: {[
            project.path_with_namespace
            for project 
            in models
        ]}")
    return models
