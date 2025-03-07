from typing import TypeVar, Any, cast

from django.db.models import QuerySet, Model

ClassType = TypeVar('ClassType', bound=Model)


def cast_query_set(
        typ: type[ClassType],
        val: Any
) -> QuerySet[ClassType]:
    return cast(
        typ=QuerySet[typ],
        val=val
    )
