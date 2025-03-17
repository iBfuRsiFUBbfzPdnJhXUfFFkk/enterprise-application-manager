from typing import TypedDict

from git_lab.models.common.typed_dicts.git_lab_time_stats_typed_dict import GitLabTimeStatsTypedDict


class BaseGitLabTimeStatsTypedDict(TypedDict):
    time_stats: GitLabTimeStatsTypedDict | None
