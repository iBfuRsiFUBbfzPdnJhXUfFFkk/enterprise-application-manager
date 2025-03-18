from typing import cast, TypedDict

from core.utilities.convert_and_enforce_utc_timezone import convert_and_enforce_utc_timezone
from git_lab.apis.common.typed_dict_to_model.assignees_to_model import assignees_to_model
from git_lab.apis.common.typed_dict_to_model.author_to_model import author_to_model
from git_lab.apis.common.typed_dict_to_model.closed_by_to_model import closed_by_to_model
from git_lab.apis.common.typed_dict_to_model.created_at_to_model import created_at_to_model
from git_lab.apis.common.typed_dict_to_model.description_to_model import description_to_model
from git_lab.apis.common.typed_dict_to_model.generic_user_to_model import generic_user_to_model
from git_lab.apis.common.typed_dict_to_model.generic_users_to_model import generic_users_to_model
from git_lab.apis.common.typed_dict_to_model.iid_to_model import iid_to_model
from git_lab.apis.common.typed_dict_to_model.state_to_model import state_to_model
from git_lab.apis.common.typed_dict_to_model.task_completion_status_to_model import task_completion_status_to_model
from git_lab.apis.common.typed_dict_to_model.time_stats_to_model import time_stats_to_model
from git_lab.apis.common.typed_dict_to_model.title_to_model import title_to_model
from git_lab.apis.common.typed_dict_to_model.updated_at_to_model import updated_at_to_model
from git_lab.apis.common.typed_dict_to_model.web_url_to_model import web_url_to_model
from git_lab.models.common.typed_dicts.git_lab_merge_request_typed_dict import GitLabMergeRequestTypedDict
from git_lab.models.common.typed_dicts.git_lab_references_typed_dict import GitLabReferencesTypedDict
from git_lab.models.git_lab_merge_request import GitLabMergeRequest
from git_lab.models.git_lab_project import GitLabProject
from scrum.models.scrum_sprint import ScrumSprint


def group_merge_request_to_model(
        typed_dict: GitLabMergeRequestTypedDict,
) -> GitLabMergeRequest | None:
    merge_request_id: int | None = typed_dict.get("id")
    if merge_request_id is None:
        return None
    get_or_create_tuple: tuple[GitLabMergeRequest, bool] = GitLabMergeRequest.objects.get_or_create(id=merge_request_id)
    instance: GitLabMergeRequest = get_or_create_tuple[0]

    instance: GitLabMergeRequest = assignees_to_model(model=instance, typed_dict=typed_dict)
    instance: GitLabMergeRequest = author_to_model(model=instance, typed_dict=typed_dict)
    instance: GitLabMergeRequest = closed_by_to_model(model=instance, typed_dict=typed_dict)
    instance: GitLabMergeRequest = created_at_to_model(model=instance, typed_dict=typed_dict)
    instance: GitLabMergeRequest = description_to_model(model=instance, typed_dict=typed_dict)
    instance: GitLabMergeRequest = iid_to_model(model=instance, typed_dict=typed_dict)
    instance: GitLabMergeRequest = state_to_model(model=instance, typed_dict=typed_dict)
    instance: GitLabMergeRequest = task_completion_status_to_model(model=instance, typed_dict=typed_dict)
    instance: GitLabMergeRequest = time_stats_to_model(model=instance, typed_dict=typed_dict)
    instance: GitLabMergeRequest = title_to_model(model=instance, typed_dict=typed_dict)
    instance: GitLabMergeRequest = updated_at_to_model(model=instance, typed_dict=typed_dict)
    instance: GitLabMergeRequest = web_url_to_model(model=instance, typed_dict=typed_dict)

    instance.blocking_discussions_resolved = typed_dict.get("blocking_discussions_resolved")
    instance.draft = typed_dict.get("draft")
    instance.has_conflicts = typed_dict.get("has_conflicts")
    instance.sha = typed_dict.get("sha")
    instance.source_branch = typed_dict.get("source_branch")
    instance.target_branch = typed_dict.get("target_branch")
    instance.closed_at = convert_and_enforce_utc_timezone(
        datetime_string=typed_dict.get("closed_at")
    )
    instance.merged_at = convert_and_enforce_utc_timezone(
        datetime_string=typed_dict.get("merged_at")
    )
    instance.prepared_at = convert_and_enforce_utc_timezone(
        datetime_string=typed_dict.get("prepared_at")
    )
    references: GitLabReferencesTypedDict | None = typed_dict.get("references")
    if references is not None:
        instance.references_long = references.get("long")
        instance.references_relative = references.get("relative")
        instance.references_short = references.get("short")
    project: GitLabProject | None = GitLabProject.objects.filter(id=typed_dict.get("project_id")).first()
    if project is not None:
        instance.project = project
        instance.group = project.group
    if instance.merged_at is not None:
        scrum_sprint: ScrumSprint | None = ScrumSprint.objects.filter(
            date_start__lte=instance.merged_at,
            date_end__gte=instance.merged_at,
        ).first()
        if scrum_sprint is not None:
            instance.scrum_sprint = scrum_sprint
    instance = generic_user_to_model(
        model=instance,
        typed_dict=cast(
            typ=TypedDict,
            val=typed_dict,
        ),
        user_model_field="merged_by",
    )
    instance = generic_users_to_model(
        model=instance,
        typed_dict=cast(
            typ=TypedDict,
            val=typed_dict,
        ),
        users_model_field="reviewers",
    )
    return instance
