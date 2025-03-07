from typing import TypeVar, Any, cast

from django.db.models import QuerySet

from core.models.common.abstract.abstract_base_model import AbstractBaseModel

ClassType = TypeVar('ClassType', bound=AbstractBaseModel)


def cast_query_set(
        typ: type[ClassType],
        val: Any
) -> QuerySet[ClassType]:
    return cast(
        typ=QuerySet[typ],
        val=val
    )
