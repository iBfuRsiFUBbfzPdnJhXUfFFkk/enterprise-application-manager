from typing import TypeVar, TypedDict

from django.db.models import Model

from git_lab.models.common.typed_dicts.git_lab_user_reference_typed_dict import GitLabUserReferenceTypedDict
from git_lab.models.git_lab_user import GitLabUser

T = TypeVar("T", bound=Model)
U = TypeVar("U", bound=TypedDict)


def generic_user_to_model(
        model: T,
        typed_dict: U,
        user_model_field: str,
) -> T:
    user_dict: GitLabUserReferenceTypedDict | None = typed_dict.get(user_model_field)
    if user_dict is None:
        return model
    user_id: int | None = user_dict.get("id")
    if user_id is None:
        return model
    user_model: GitLabUser | None = GitLabUser.objects.filter(id=user_id).first()
    if user_model is None:
        return model
    setattr(model, user_model_field, user_model)
    return model
