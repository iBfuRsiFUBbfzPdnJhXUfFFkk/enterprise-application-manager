from typing import TypedDict

from git_lab.models.common.typed_dicts.git_lab_links_typed_dict import GitLabLinksTypedDict


class BaseGitLabLinksTypedDict(TypedDict):
    _links: GitLabLinksTypedDict | None
