from typing import TypeVar

from django.db.models import Model

from git_lab.models.common.typed_dicts.bases.base_git_lab_time_stats_typed_dict import BaseGitLabTimeStatsTypedDict
from git_lab.models.common.typed_dicts.git_lab_time_stats_typed_dict import GitLabTimeStatsTypedDict

T = TypeVar("T", bound=Model)
U = TypeVar("U", bound=BaseGitLabTimeStatsTypedDict)


def time_stats_to_model(
        model: T,
        typed_dict: U,
) -> T:
    time_stats: GitLabTimeStatsTypedDict | None = typed_dict.get("time_stats")
    if time_stats is None:
        return model
    model.time_stats_human_time_estimate = time_stats.get("human_time_estimate")
    model.time_stats_human_total_time_spent = time_stats.get("human_total_time_spent")
    model.time_stats_time_estimate = time_stats.get("time_estimate")
    model.time_stats_total_time_spent = time_stats.get("total_time_spent")
    return model
