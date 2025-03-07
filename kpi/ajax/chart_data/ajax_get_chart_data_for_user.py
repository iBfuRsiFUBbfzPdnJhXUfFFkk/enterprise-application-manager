from django.http import JsonResponse, HttpRequest, HttpResponse

from core.models.person import Person
from core.views.generic.generic_500 import generic_500
from kpi.ajax.chart_data.common.chart_data_model import ChartDataModel
from kpi.ajax.chart_data.common.get_chart_data_for_person import get_chart_data_for_person


def ajax_get_chart_data_for_user(
        request: HttpRequest,
        uuid: str
) -> JsonResponse | HttpResponse:
    person: Person | None = Person.from_uuid(uuid=uuid)
    if person is None:
        return generic_500(request=request)
    data: ChartDataModel | None = get_chart_data_for_person(person=person)
    if data is None:
        return generic_500(request=request)
    return JsonResponse(data=data)
