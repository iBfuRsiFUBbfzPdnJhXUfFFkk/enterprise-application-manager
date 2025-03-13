from datetime import datetime, timezone
from typing import TypedDict

from django.http import HttpRequest, QueryDict


class GitLabApiCommonQueryParameters(TypedDict):
    all: bool | None
    assignee_id: int | None
    author_id: int | None
    created_after: datetime | None
    created_before: datetime | None
    get_all: bool | None
    iteration_id: int | None
    order_by: str | None
    page: int | None
    per_page: int | None
    sort: str | None
    state: str | None
    updated_after: datetime | None
    updated_before: datetime | None


def get_initial_gitlab_api_common_query_parameters() -> GitLabApiCommonQueryParameters:
    return {
        "all": True,
        "assignee_id": None,
        "author_id": None,
        "created_after": None,
        "created_before": None,
        "get_all": True,
        "iteration_id": None,
        "order_by": "updated_at",
        "page": None,
        "per_page": None,
        "sort": "desc",
        "state": None,
        "updated_after": None,
        "updated_before": None,
    }


def get_common_query_parameters(
        request: HttpRequest | None = None
) -> GitLabApiCommonQueryParameters:
    return_dict: GitLabApiCommonQueryParameters = get_initial_gitlab_api_common_query_parameters()
    if request is None:
        return return_dict
    query_dict: QueryDict = request.GET
    return_dict["all"] = query_dict.get('all', True)
    return_dict["assignee_id"] = query_dict.get('assignee_id', None)
    return_dict["author_id"] = query_dict.get('author_id', None)
    return_dict["iteration_id"] = query_dict.get('iteration_id', None)
    return_dict["get_all"] = query_dict.get('all', True)
    return_dict["order_by"] = query_dict.get('updated_at', None)
    return_dict["page"] = query_dict.get('page', None)
    return_dict["per_page"] = query_dict.get('per_page', None)
    return_dict["sort"] = query_dict.get('sort', "desc")
    return_dict["state"] = query_dict.get('state', "all")
    created_before: str | None = query_dict.get('created_before', None)
    created_after: str | None = query_dict.get('created_after', None)
    updated_after: str | None = query_dict.get('updated_after', None)
    updated_before: str | None = query_dict.get('updated_before', None)
    utc: timezone = timezone.utc
    date_format: str = "%Y-%m-%d"
    if created_before is not None:
        return_dict["created_before"] = datetime.strptime(created_before, date_format).replace(tzinfo=utc)
    if created_after is not None:
        return_dict["created_after"] = datetime.strptime(created_after, date_format).replace(tzinfo=utc)
    if updated_after is not None:
        return_dict["updated_after"] = datetime.strptime(updated_after, date_format).replace(tzinfo=utc)
    if updated_before is not None:
        return_dict["updated_before"] = datetime.strptime(updated_before, date_format).replace(tzinfo=utc)
    return return_dict
