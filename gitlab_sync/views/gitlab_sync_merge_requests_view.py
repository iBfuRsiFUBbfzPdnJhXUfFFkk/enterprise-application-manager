from django.http import HttpRequest, HttpResponse

from core.utilities.base_render import base_render
from gitlab_sync.models import GitLabSyncMergeRequest


def gitlab_sync_merge_requests_view(request: HttpRequest) -> HttpResponse:
    """
    GitLab Merge Requests list view with search and filtering.
    """
    search_query = request.GET.get("search", "").strip()
    state_filter = request.GET.get("state", "").strip()
    draft_filter = request.GET.get("draft", "").strip()

    merge_requests = GitLabSyncMergeRequest.objects.all().select_related(
        "project", "author", "head_pipeline"
    ).prefetch_related("assignees", "reviewers").order_by("-updated_at")

    if search_query:
        merge_requests = merge_requests.filter(title__icontains=search_query)

    if state_filter:
        merge_requests = merge_requests.filter(state=state_filter)

    if draft_filter == "true":
        merge_requests = merge_requests.filter(draft=True)
    elif draft_filter == "false":
        merge_requests = merge_requests.filter(draft=False)

    return base_render(
        request=request,
        template_name="authenticated/gitlab_sync/merge_requests.html",
        context={
            "merge_requests": merge_requests,
            "total_count": merge_requests.count(),
            "search_query": search_query,
            "state_filter": state_filter,
            "draft_filter": draft_filter,
        },
    )
