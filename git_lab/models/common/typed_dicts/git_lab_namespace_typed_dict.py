from git_lab.models.common.typed_dicts.bases.base_git_lab_id_typed_dict import BaseGitLabIdTypedDict


class GitLabNamespaceTypedDict(BaseGitLabIdTypedDict, ):
    kind: str | None
