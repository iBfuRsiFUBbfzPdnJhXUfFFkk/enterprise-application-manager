from typing import TypeVar, Any, cast

from django.db.models import QuerySet

from core.models.common.abstract.base_model import BaseModel

ClassType = TypeVar('ClassType', bound=BaseModel)


def cast_query_set(
        typ: type[ClassType],
        val: Any
) -> QuerySet[ClassType]:
    return cast(
        typ=QuerySet[typ],
        val=val
    )
