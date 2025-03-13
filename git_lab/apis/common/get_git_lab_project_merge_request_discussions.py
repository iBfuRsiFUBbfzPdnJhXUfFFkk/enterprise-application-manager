from typing import cast

from gitlab import GitlabListError, GitlabAuthenticationError
from gitlab.base import RESTObjectList
from gitlab.v4.objects import ProjectMergeRequest, ProjectMergeRequestDiscussion

from core.settings.common.developer import DEBUG


def get_git_lab_project_merge_request_discussions(
        all_project_merge_requests: list[ProjectMergeRequest]
) -> list[ProjectMergeRequestDiscussion]:
    all_discussions: set[ProjectMergeRequestDiscussion] = set()
    for project_merge_request in all_project_merge_requests:
        try:
            discussion_generator: RESTObjectList = project_merge_request.discussions.list(
                iterator=True,
            )
            for discussion in discussion_generator:
                if DEBUG is True and discussion not in all_discussions:
                    print(f"discussion: {discussion.asdict().get("id")}")
                all_discussions.add(
                    cast(
                        typ=ProjectMergeRequestDiscussion,
                        val=discussion,
                    )
                )
        except GitlabListError as error:
            print(f"GitLabListError on {project_merge_request.asdict().get("id")}: {error.error_message}")
            continue
        except GitlabAuthenticationError as error:
            print(f"GitlabAuthenticationError on {project_merge_request.asdict().get("id")}: {error.error_message}")
            continue
    return list(all_discussions)
