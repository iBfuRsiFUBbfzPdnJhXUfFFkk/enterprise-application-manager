from django.http import HttpRequest, HttpResponse

from core.models.person import Person
from core.utilities.base_render import base_render
from core.views.generic.generic_500 import generic_500


def kpi_person_view(request: HttpRequest, uuid: str) -> HttpResponse:
    person: Person | None = Person.get_by_uuid(uuid=uuid)
    if person is None:
        return generic_500(request=request)
    return base_render(
        context={
            "person": person,
        },
        request=request,
        template_name="authenticated/kpi/kpi_person.html"
    )
