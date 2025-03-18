from typing import TypeVar, TypedDict

from django.db.models import Model

from git_lab.models.common.typed_dicts.git_lab_user_reference_typed_dict import GitLabUserReferenceTypedDict
from git_lab.models.git_lab_user import GitLabUser

T = TypeVar("T", bound=Model)
U = TypeVar("U", bound=TypedDict)


def generic_users_to_model(
        model: T,
        typed_dict: U,
        users_model_field: str,
) -> T:
    user_dicts: list[GitLabUserReferenceTypedDict] | None = typed_dict.get(users_model_field)
    if user_dicts is None:
        return model
    for user_dict in user_dicts:
        user_id: int | None = user_dict.get("id")
        if user_id is None:
            continue
        user_model: GitLabUser | None = GitLabUser.objects.filter(id=user_id).first()
        if user_model is None:
            continue
        getattr(model, users_model_field).add(user_model)
    return model
